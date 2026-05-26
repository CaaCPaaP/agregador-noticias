import feedparser
import requests
from datetime import datetime
from django.utils import timezone
from django.template.defaultfilters import slugify
from decouple import config
from celery import shared_task
from .models import Article, Category
from sources.models import Source

def parse_date(date_string):
    if not date_string:
        return timezone.now()
    try:
        from email.utils import parsedate_to_datetime
        dt =parsedate_to_datetime(date_string)
        if timezone.is_naive(dt):
            dt = timezone.make_aware(dt, timezone=timezone.utc)
        return dt
    except Exception:
        return timezone.now()

@shared_task
def fetch_rss_source(source_id):
    try:
        source = Source.objects.get(id=source_id, is_active=True, is_rss=True)
        feed = feedparser.parse(source.url)
        created_count = 0

        for entry in feed.entries:
            url = entry.get('link', '')
            if not url or Article.objects.filter(url=url).exists():
                continue
    
            Article.objects.create(
                title=entry.get('title', '')[:500],
                url=url,
                description=entry.get('summary', ''),
                author=entry.get('author', ''),
                source=source,
                published_at=parse_date(entry.get('published')),
            )
            created_count += 1

        return f'{source.name}: {created_count} novos artigos.'
    except Source.DoesNotExist:
        return f'Fonte {source_id} não encontrada.'
    except Exception as e:
        return f'Erro: {str(e)}'
    
@shared_task
def fetch_newsapi(query='technology', language='pt', page_size=20):
    api_key = config('NEWSAPI_KEY', default='')
    if not api_key:
        return 'NEWSAPI_KEY não configurada.'
    
    try:
        response = requests.get(
            'https://newsapi.org/v2/everything',
            params={
                'q': query,
                'language': language,
                'pageSize': page_size,
                'apiKey': api_key,
            },
            timeout=10
        )
        data = response.json()

        if data.get('status') != 'ok':
            return f'Erro NewsAPI: {data.get("message")}'
        
        category_name = query.capitalize()
        category, _ = Category.objects.get_or_create(
            slug=slugify(category_name),
            defaults={'name': category_name}
        )

        source, _ = Source.objects.get_or_create(
            url = 'https://newsapi.org',
            defaults={'name': 'NewsAPI', 'is_rss': False}
        )

        created_count = 0
        for article_data in data.get('articles', []):
            url = article_data.get('url', '')
            if not url or url == ['removed']:
                continue
            if Article.objects.filter(url=url).exists():
                continue
        
            Article.objects.create(
                title=article_data.get('title', '')[:500],
                url=url,
                description=article_data.get('description', '') or '',
                author=article_data.get('author', '') or '',
                image_url=article_data.get('urlToImage', '') or '',
                source=source,
                category=category,
                published_at=timezone.now(),
            )
            created_count += 1
 
        return f'NewsAPI: ({query}): {created_count} novos artigos.'
    except Exception as e:
        return f'Erro: {str(e)}'
    
@shared_task
def fetch_all_news():
    results = []

    rss_sources = Source.objects.filter(is_active=True, is_rss=True)
    for source in rss_sources:
        result = fetch_rss_source(source.id)
        results.append(result)

    for query in ['tecnologia', 'brasil', 'ciencia', 'economia']:
        result = fetch_newsapi(query=query)
        results.append(result)

    return results
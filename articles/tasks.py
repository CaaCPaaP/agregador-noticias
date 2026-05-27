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
    """Converte uma string de data de feed RSS para datetime com timezone.

    Feeds RSS usam o formato RFC 2822 (ex: 'Mon, 26 May 2026 10:00:00 +0000').
    Se a conversão falhar por qualquer motivo, retorna a data/hora atual.

    Args:
        date_string: string de data vinda do feed RSS

    Returns:
        datetime com timezone configurado
    """

    if not date_string:
        return timezone.now()
    try:
        from email.utils import parsedate_to_datetime
        dt =parsedate_to_datetime(date_string)
        # Alguns feeds retornam datas sem timezone — adicionamos UTC nesses casos
        if timezone.is_naive(dt):
            dt = timezone.make_aware(dt, timezone=timezone.utc)
        return dt
    except Exception:
        return timezone.now()

@shared_task
def fetch_rss_source(source_id):
    """Coleta artigos de uma fonte RSS e salva no banco.

    Busca apenas fontes ativas. Ignora artigos já existentes
    usando a URL como chave de deduplicação.

    Args:
        source_id: ID da Source com is_rss=True

    Returns:
        str: mensagem com quantidade de artigos salvos ou descrição do erro
    """

    try:
        source = Source.objects.get(id=source_id, is_active=True, is_rss=True)
        feed = feedparser.parse(source.url)
        created_count = 0

        for entry in feed.entries:
            url = entry.get('link', '')
            if not url or Article.objects.filter(url=url).exists(): # Pula entradas sem URL ou já existentes no banco (deduplicação)
                continue
    
            Article.objects.create(
                title=entry.get('title', '')[:500], # Limita ao max_length do campo
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
    """Coleta artigos da NewsAPI e salva no banco.

    Cria automaticamente a categoria e a fonte 'NewsAPI' se não existirem.
    Ignora artigos já existentes usando a URL como chave de deduplicação.

    Args:
        query: termo de busca (ex: 'tecnologia')
        language: idioma dos artigos ('pt', 'en', etc.)
        page_size: quantidade máxima de artigos por chamada (máx. 100 no plano gratuito)

    Returns:
        str: mensagem com quantidade de artigos salvos ou descrição do erro
    """

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
            timeout=10 # Evita que a task fique travada em caso de lentidão da API
        )
        data = response.json()

        if data.get('status') != 'ok':
            return f'Erro NewsAPI: {data.get("message")}'
        
        # Cria a categoria com base no termo de busca, se ainda não existir
        category_name = query.capitalize()
        category, _ = Category.objects.get_or_create(
            slug=slugify(category_name),
            defaults={'name': category_name}
        )

        # Usa uma única Source para todos os artigos vindos da NewsAPI
        source, _ = Source.objects.get_or_create(
            url = 'https://newsapi.org',
            defaults={'name': 'NewsAPI', 'is_rss': False}
        )

        created_count = 0
        for article_data in data.get('articles', []):
            url = article_data.get('url', '')
            # Pula artigos sem URL, removidos pela NewsAPI ou já existentes no banco
            if not url or url == ['removed']:
                continue
            if Article.objects.filter(url=url).exists():
                continue
        
            Article.objects.create(
                title=article_data.get('title', '')[:500], # Limita ao max_length do campo
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
    """Executa a coleta completa de todas as fontes ativas.

    Chamada automaticamente pelo Celery Beat a cada 30 minutos
    conforme configurado em CELERY_BEAT_SCHEDULE no settings.py.

    Returns:
        list: resultados de cada coleta individual
    """

    results = []

    # Coleta de todas as fontes RSS cadastradas e ativas no banco
    rss_sources = Source.objects.filter(is_active=True, is_rss=True)
    for source in rss_sources:
        result = fetch_rss_source(source.id)
        results.append(result)

    # Coleta da NewsAPI para cada tema de interesse
    for query in ['tecnologia', 'brasil', 'ciencia', 'economia']:
        result = fetch_newsapi(query=query)
        results.append(result)

    return results
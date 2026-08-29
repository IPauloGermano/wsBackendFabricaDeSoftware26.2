import re
import requests
from django.db.models import Q
from .models import Livro
OPENLIBRARY_BASE_URL = 'https://openlibrary.org'
TIMEOUT = 6.0

def _get(endpoint, params=None):
    url = f"{OPENLIBRARY_BASE_URL}/{endpoint.lstrip('/')}"
    try:
        response = requests.get(url, params=params, timeout=TIMEOUT)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f'Erro ao chamar Open Library ({url}): {e}')
        return None

def _normalizar_openlibrary_id(raw_id):
    if not raw_id:
        return ''
    clean = raw_id.strip()
    clean = re.sub('^/?works/', '', clean)
    return clean.strip('/')

def _extrair_descricao(raw_description):
    if not raw_description:
        return ''
    if isinstance(raw_description, str):
        return raw_description.strip()
    if isinstance(raw_description, dict):
        return str(raw_description.get('value', '')).strip()
    return str(raw_description).strip()

def _extrair_ano(date_str):
    if not date_str:
        return None
    if isinstance(date_str, int):
        return date_str
    match = re.search('\\b(1\\d{3}|20\\d{2})\\b', str(date_str))
    return int(match.group(1)) if match else None

def _resolver_autores(authors_data):
    if not authors_data or not isinstance(authors_data, list):
        return 'Autor desconhecido'
    nomes = []
    for item in authors_data[:3]:
        if isinstance(item, dict):
            author_ref = item.get('author', {})
            author_key = author_ref.get('key', '') if isinstance(author_ref, dict) else ''
            if author_key:
                try:
                    clean_key = author_key.replace('/authors/', '').replace('authors/', '').strip()
                    author_info = _get(f'/authors/{clean_key}.json')
                    if author_info:
                        name = author_info.get('name') or author_info.get('personal_name')
                        if name:
                            nomes.append(name)
                except Exception:
                    pass
    return ', '.join(nomes) if nomes else 'Autor desconhecido'

def buscar_na_openlibrary(query, limit=16):
    if not query or not query.strip():
        return {'livros': [], 'total': 0, 'erro': None}
    params = {'q': query.strip(), 'limit': limit, 'page': 1, 'fields': 'key,title,author_name,first_publish_year,cover_i,isbn,publisher,subject'}
    try:
        raw_data = _get('/search.json', params=params)
        if not raw_data:
            raise Exception('Resposta vazia da API')
        docs = raw_data.get('docs', [])
        total = raw_data.get('numFound', len(docs))
        livros = []
        for doc in docs:
            openlibrary_id = _normalizar_openlibrary_id(doc.get('key', ''))
            if not openlibrary_id:
                continue
            cover_i = doc.get('cover_i')
            capa_url = f'https://covers.openlibrary.org/b/id/{cover_i}-M.jpg' if cover_i else ''
            author_names = doc.get('author_name', [])
            autores = ', '.join(author_names) if author_names else 'Autor desconhecido'
            isbns = doc.get('isbn', [])
            isbn = isbns[0] if isbns else ''
            publishers = doc.get('publisher', [])
            editora = ', '.join(publishers[:3]) if publishers else ''
            subjects = doc.get('subject', [])
            assuntos = ', '.join(subjects[:5]) if subjects else ''
            livros.append({'openlibrary_id': openlibrary_id, 'titulo': doc.get('title', 'Sem título'), 'autores': autores, 'capa_url': capa_url, 'isbn': isbn, 'editora': editora, 'ano_publicacao': doc.get('first_publish_year'), 'assuntos': assuntos, 'descricao': ''})
        return {'livros': livros, 'total': total, 'erro': None}
    except Exception as e:
        print(f'Erro ao buscar na OpenLibrary: {e}')
        return {'livros': [], 'total': 0, 'erro': 'Não foi possível carregar os livros da Open Library.'}

def buscar_detalhes_openlibrary(openlibrary_id):
    clean_id = _normalizar_openlibrary_id(openlibrary_id)
    if not clean_id:
        return None
    try:
        work_data = _get(f'/works/{clean_id}.json')
        if not work_data:
            return None
        covers = work_data.get('covers', [])
        capa_url = ''
        if covers and isinstance(covers, list) and (covers[0] > 0):
            capa_url = f'https://covers.openlibrary.org/b/id/{covers[0]}-L.jpg'
        descricao = _extrair_descricao(work_data.get('description', ''))
        subjects = work_data.get('subjects', [])
        assuntos = ', '.join(subjects[:8]) if isinstance(subjects, list) else ''
        ano_publicacao = _extrair_ano(work_data.get('first_publish_date'))
        autores = _resolver_autores(work_data.get('authors', []))
        return {'openlibrary_id': clean_id, 'titulo': work_data.get('title', 'Sem título'), 'autores': autores, 'capa_url': capa_url, 'isbn': '', 'editora': '', 'ano_publicacao': ano_publicacao, 'descricao': descricao or 'Descrição não informada.', 'assuntos': assuntos}
    except Exception as e:
        print(f'Erro ao pegar detalhes do livro {clean_id}: {e}')
        return None

def buscar_catalogo(termo='', buscar_na_api=True):
    termo = termo.strip() if termo else ''
    if termo:
        livros_locais = list(Livro.objects.filter(Q(titulo__icontains=termo) | Q(autores__icontains=termo) | Q(assuntos__icontains=termo) | Q(openlibrary_id__iexact=termo)))
    else:
        livros_locais = list(Livro.objects.all()[:30])
    ids_locais = {livro.openlibrary_id for livro in livros_locais if livro.openlibrary_id}
    livros_remotos = []
    erro_api = None
    if buscar_na_api:
        termo_busca = termo if termo else 'classic literature'
        resultado = buscar_na_openlibrary(termo_busca, limit=16)
        erro_api = resultado.get('erro')
        for livro_api in resultado.get('livros', []):
            ol_id = livro_api['openlibrary_id']
            if ol_id in ids_locais:
                continue
            if Livro.objects.filter(openlibrary_id=ol_id).exists():
                continue
            livros_remotos.append(livro_api)
    return {'termo': termo, 'livros_locais': livros_locais, 'livros_remotos': livros_remotos, 'erro_api': erro_api, 'total_locais': len(livros_locais), 'total_remotos': len(livros_remotos)}

def obter_ou_criar_livro(openlibrary_id, fallback_data=None):
    clean_id = _normalizar_openlibrary_id(openlibrary_id)
    if not clean_id:
        return None
    livro = Livro.objects.filter(openlibrary_id=clean_id).first()
    if livro:
        return livro
    dados = None
    try:
        dados = buscar_detalhes_openlibrary(clean_id)
    except Exception as e:
        print(f'Erro ao buscar na openlibrary: {e}')
    if not dados and fallback_data:
        dados = fallback_data
    if not dados:
        return None
    livro = Livro.objects.create(openlibrary_id=clean_id, titulo=dados.get('titulo') or 'Sem título', autores=dados.get('autores') or 'Autor desconhecido', capa_url=dados.get('capa_url') or '', isbn=dados.get('isbn') or '', editora=dados.get('editora') or '', ano_publicacao=dados.get('ano_publicacao'), descricao=dados.get('descricao') or '', assuntos=dados.get('assuntos') or '')
    return livro
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import News, NewsPageText


def news_list(request):
    news_list = News.objects.filter(is_published=True).order_by('-created_at')
    paginator = Paginator(news_list, 5)  # Show 5 news per page
    page_number = request.GET.get('page')
    news_page = paginator.get_page(page_number)
    news_text = NewsPageText.objects.first()
    
    return render(request, 'news/list.html', {
        'news_page': news_page,
        'news_text': news_text,
    })


def news_detail(request, pk):
    news = get_object_or_404(News, pk=pk, is_published=True)
    news_text = NewsPageText.objects.first()
    
    return render(request, 'news/detail.html', {
        'news': news,
        'news_text': news_text,
    })

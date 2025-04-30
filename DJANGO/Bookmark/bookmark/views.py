from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from bookmark.models import Bookmark


def bookmark_list(request):
    bookmarks = Bookmark.objects.all()
    # SELECT * FROM bookmark
    context = {
        'bookmarks' : bookmarks
    }
    return render(request, template_name='bookmark_list.html', context=context)

def bookmark_detail(request, pk):
    # try:
    #     bookmark = Bookmark.objects.get(pk=pk)
    # except:
    #     raise Http404
    bookmark = get_object_or_404(Bookmark, pk=pk)
    context = {
        'bookmark' : bookmark
    }
    return render(request, template_name='bookmark_detail.html', context=context)

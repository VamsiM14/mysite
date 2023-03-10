from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm

# Create your views here.
def post_list(request):
    post_list = Post.published.all()
    # Pagination with 3 posts per page
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number) 
    except(EmptyPage):
        # Handle out of range pages
        posts = paginator.page(paginator.num_pages)
    except(PageNotAnInteger):
        # Handle non-integer page inputs
        posts = paginator.page(1)  
    return render(
        request,
        'blog/post/list.xhtml',
        {'posts': posts} 
    )

def post_share(request, post_id):
    # Retrive post by id
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
        )
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST):
        if form.is_valid():
            cd = form.cleaned_data
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.xhtml', {'form': form})

class PostListView(ListView):
    '''
    Alternative post list view
    '''
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.xhtml'
    

def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day)

    return render(
        request,
        'blog/post/detail.xhtml',
        {'post': post} )
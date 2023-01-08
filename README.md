# app_fin_trainer
app_fin_trainer

command examples:
>>> User.objects.create_user(username = 'User #2')
<User: User #2>
>>> User.objects.create_user(username = 'User #3')
<User: User #3>
>>> User.objects.create_user(username = 'User #4')
<User: User #4>
>>> User.objects.create_user(username = 'grisha')

>>> Author.objects.create(authorUser=User.objects.get(id=3))
<Author: Author object (2)>
>>> Author.objects.create(authorUser=User.objects.get(id=4))
<Author: Author object (3)>
>>> Author.objects.create(authorUser=User.objects.get(id=5))
<Author: Author object (4)>

>>> Category.objects.create(name = 'Trading')
<Category: Category object (1)>
>>> Category.objects.create(name = 'News')
<Category: Category object (2)>
>>> Category.objects.create(name = 'Information')
<Category: Category object (3)>
>>> Category.objects.create(name = 'Case')
<Category: Category object (4)>

>>> Post.objects.create(author = author, categoryType = 'NW', postTitle = 'my first title', postText = 'my first post text')
<Post: Post object (1)>
>>> Post.objects.get(id=1).postText
'my first post text'
>>> Post.objects.create(author = Author.objects.get(id=3), categoryType = 'AR', postTitle = 'article 1', postText = 'my first article text')
<Post: Post object (2)>
>>> Post.objects.create(author = Author.objects.get(id=3), categoryType = 'AR', postTitle = 'article 2', postText = 'my second article text')
<Post: Post object (3)>

>>> Post.objects.get(id=1).postCategory.add(Category.objects.get(id=2))
>>> Post.objects.get(id=2).postCategory.add(Category.objects.get(id=2))
>>> Post.objects.get(id=2).postCategory.add(Category.objects.get(id=3))
>>> Post.objects.get(id=3).postCategory.add(Category.objects.get(id=4))

>>> Comment.objects.create(commentPost = Post.objects.get(id=1), commentUser=Author.objects.get(id=1).authorUser, commentText='this my first comment')
<Comment: Comment object (1)>
>>> Comment.objects.create(commentPost = Post.objects.get(id=2), commentUser=Author.objects.get(id=1).authorUser, commentText='this my second comment')
<Comment: Comment object (2)>
>>> Comment.objects.create(commentPost = Post.objects.get(id=3), commentUser=Author.objects.get(id=1).authorUser, commentText='this my second comment')
<Comment: Comment object (3)>

>>> Comment.objects.get(id=1).like()
>>> Comment.objects.get(id=1).rating
Traceback (most recent call last):
  File "<console>", line 1, in <module>
AttributeError: 'Comment' object has no attribute 'rating'
>>> Comment.objects.get(id=1).commentRating
1
>>> Comment.objects.get(id=1).dislike()
>>> Comment.objects.get(id=1).dislike()
>>> Comment.objects.get(id=1).commentRating
-1
>>> Author.objects.get(id=1).ratingAuthor
0
>>> a= Author.objects.get(id=1)
>>> a.update_rating()
>>> a.ratingAuthor
-0.5
>>> Post.objects.get(id=1).like()
>>> Post.objects.get(id=1).like()
>>> a.update_rating()
>>> a.ratingAuthor
0.5

>>> q = Author.objects.order_by('-ratingAuthor')
>>> for i in q:
...     print(i.authorUser)
... 
grisha
User #2
User #3
User #4
>>> 


qpost = Post.objects.order_by('-postRating')
>>> for i in qpost:
...     print(Author.objects.get(id=i.author_id).authorUser)
...     print(i.postRating)
...     print(i.preview())
...     print(i.postTitle)
... 
grisha
2
my first post text ...
my first title
User #3
0
my first article text ...
article 1
User #3
0
my second article text ...
article 2

>>> qcomment=Comment.objects.filter(commentUser=Author.objects.get(id=1).authorUser)
>>> for i in qcomment:
...     print(i.commentText)
... 
this my first comment
this my second comment
this my second comment
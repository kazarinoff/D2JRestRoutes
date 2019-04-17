# DjangoRestRoutes
A module to translate Django model objects into JSON restful endpoints

## To use:
1. Pull file into app folder it's to be used for.

2. In app URLs file, Import RestfulModel, along w/ your Django Model object

3. Create a local RestfulModel from the Django Model
    
    myapi=RestfulModel(MyModel)
    
4a. Easiest- set URL parameters to include default_routes() method (this outputs an array of django paths: index/,<id>/,create/,<id>/edit/,<id>/delete/,search/,random/,).
    
    path('',include(myapi.default_routes()))
    
4b. Set individual URLs to use object methods as views- available methods are:index,show,create,edit,delete,search,random. Note that show, edit, and delete require an <eid> to be included in the route url.
    
    path('index',myapi.index,name='index')

## Notes:
Be sure to makemigrations and migrate

Create, edit, & search routes take params from request to do their thing

default_routes() takes optional post & crsf variables, defaults to False. 
    If post is True, create, edit,& delete routes will only accept post requests. If crsf is True, post requests must be validated to be       accepted (I dont think this feature is actually working but maybe kinda)

## Still to implement:

~~random route~~
~~search route~~

accept apikey in some form

finish crsf ability

package/modulize it

deal w/ manytomany relationships

~~add response status codes~~


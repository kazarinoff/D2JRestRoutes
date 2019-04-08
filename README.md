# DjangoRestRoutes
A brief file to transfer Django model objects into restful endpoints

## To use:
1.Pull file into app folder it's to be used in
2.In app URLs file, Import RestfulModel, along w/ your Django Model object
3.create a local RestfulModel from the Django Model
    myapi=RestfulModel(mymodel)
4a.Set URL parameters to include default_routes() method
    path('',include(myapi.default_routes()))
4b.Set individual URLs to use object methods as views(methods are:index,show,create,edit,delete)
    path('index',mymodel.index,name='index')

(4c.Individual URLS can be set to include individual routes methods
    path('',include(myapi.index(name=all)))
still working on how this presents...)

## Notes:
Be sure to makemigrations and migrate
default_routes() takes optional post & crsf variables, defaults to False. If post is True, create, edit,& delete routes will only accept post requests. If crsf is True, post requests must be validated to be accepted (I dont think this feature is actually working but maybe kinda)
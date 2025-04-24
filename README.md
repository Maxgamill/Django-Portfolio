# Django-Portfolio

The source code for my portfolio website highlighting some academic and side 
projects I completed at University.

## Summary
Watch the short video below which takes you on a short tour of the site:

![site_tour.mov](site_tour.mov)

## Installation Instructions
As the webserver is currently down to enable new projects, please follow the
instructions below to run the Django webserver locally.

1. First clone this repository into a directory. You must have [git installed](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git):
```
git clone https://github.com/Maxgamill/Django-Portfolio.git
```

2. Then move into the cloned repository and create a new conda environment using the environment yaml file. You must have [Conda](https://docs.conda.io/projects/conda/en/stable/user-guide/install/index.html) (or PyEnv) for this step:
```
cd Django-Portfolio
```
```
conda env create -f env/Django-Portfolio.yml
```
```
conda activate Django-Portfolio
```

3. Run the Django development server:
```
python manage.py runserver
```

The local Django webserver should now be accessible via the local host address specified in the commandline output.

This is usually: http://127.0.0.1:8000

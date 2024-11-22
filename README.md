Pour run l'application 
1.créer un environnement virtuel 
2. pip install -r requirements.txt INSTALLER LES DEPENDANCES
3.aller dans api_connect et lancer : uvicorn main:app --reload port 8001
4.aller dans MicroService/Medical_Summirizer et lancer : python app.py (ceci devra rouler sur localhost 5000)
5. enfin dans le dossier principal lancer python manage.py runserver

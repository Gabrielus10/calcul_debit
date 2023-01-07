# Bonjour, ce code permet de faire une étude sur la chronique des débits avec les données mesurées à la station H2452010
# Fichier utulisé 'H2452010.csv' et renommé en 'Donnees.csv' comporte les données de débits journaliers en m3/s de la
# période 1900-1998. Le but est de pouvoir faire une étude entre deux dates qu'on choisira de d'afficher les graphiques
# de débits journiers, de débits max annuels, de la loi de Gumbel et un box-plot On déterminera aussi les débits max et
# min de la période choisie, les débits de périodes de retour (2,5,10,20,50,100,200,500,et 1000ans) qu'on récupérera
# dans un fichier de sortie.


#######################################################################################################################
###############################Import des modules necessaires pour la réalisation du projet############################
#######################################################################################################################
from tkinter import SUNKEN

from pylab import *
import matplotlib.pyplot as plt
from datetime import date, timedelta
import matplotlib.dates as mdates
import numpy as np 
import tkinter as tk
import tkinter.ttk as ttk
import csv
from tkinter.filedialog import *
from PIL import Image, ImageTk



##################################input-temps###########################################################

def hydro ():
    t=v.get()
    ann_dd=ann_d.get()
    ann_ff=ann_f.get()
    moisss=moiss.get()

    if t=='ans' :
        ann=int(ann_dd)
        ann2=int(ann_ff)
        dann=ann2-ann
        #Jour de depart
        day = 1
        month = 1
        year = ann
        step=30 #parametre affichage axe x graph 1
    elif t=='an':
        ann=int(ann_ff)
        ann2=str(ann)
        #Jour de depart
        day = 1
        month = 1
        year = ann
        step=15 #parametre affichage axe x graph 1
    elif t=='mois':
        ann=int(ann_ff)
        ann2=str(ann)
        mois=int(moisss)
        mois2=str(mois)
        #Jour de depart
        day = 1
        month = mois
        year = ann
        step=1 #parametre affichage axe x graph 1

    ####################################################################################################################
    ########################################  creation de Listes pour les débits et la date  ###########################
    ####################################################################################################################

    #Variables 
    debit_list = []
    date_list = []
    debit_date=[] 

    i=0
    j=0

    #Liste debit, input - temps > 1 an
    if t=='ans' :
        while i<=dann :
            ann2=str(ann)
            
            with open('Donnees.csv') as file:
                for line in file.readlines():
                    line = line.split(';')
                    if line[3] == ann2 :
                        debit_list.append(float(line[5]))            
            ann=ann+1
            i=i+1
            
        #boucle date
        d = date(year, month, day)
        while j<len(debit_list):
            debit_date.append(d.strftime('%d %m %Y'))
            d += timedelta(days=1)
            j=j+1

      
    #Liste debit, input - temps = 1 an  
    elif t=='an' :
        with open('Donnees.csv') as file:
            for line in file.readlines():
                line = line.split(';')
                if line[3] == ann2 :
                    debit_list.append(float(line[5]))
            
        #boucle date
        d = date(year, month, day)
        while j<len(debit_list):
            debit_date.append(d.strftime('%d/%m/%Y'))
            d += timedelta(days=1)
            j=j+1
                    
    #Liste debit, input - temps < 1 an
    elif t=='mois' :
        with open('Donnees.csv') as file:
            for line in file.readlines():
                line = line.split(';')
                if line[3] == ann2 and line[2] == mois2 :
                    debit_list.append(float(line[5]))
        #boucle date
        d = date(year, month, day)
        while j<len(debit_list):
            debit_date.append(d.strftime('%d/%m/%Y'))
            d += timedelta(days=step)
            j=j+1
        # print(debit_date)
        # print(len(debit_date))
        # print(len(debit_list))
                                          
    # liste date en jour Julien
    j = 0
    while j < len(debit_list):
        date_list.append(j)
        
        j+=1

    ####################################################################################################################
    #############################################PARTIE CAULATOIRE (STATS)##############################################
    ####################################################################################################################

    #Recuperation de mon ymax pour l'affichage de mon plot 
    Qmax=max(debit_list) #débit max
    Qmin=min(debit_list) #débit min
    Qmoy=mean(debit_list) #débit moyen
    Qmed=np.percentile(debit_list,50) #médiane du boxplot
    Q1=np.percentile(debit_list,25) #premier quartile
    Q3=np.percentile(debit_list,75) #troisième quartile
    
    # creation chaines de caracteres pour le rapport d'analyse (récupération dans un doc .txt)
    chaine_Qmax = 'Le debit maximum de la periode est de : ' + str(Qmax) + ' m3/s'
    chaine_Qmin = 'Le debit minimum de la periode est de : ' + str(Qmin) + ' m3/s'
    chaine_Qmoy = 'Le debit moyen de la periode est de : ' + str(Qmoy) + ' m3/s'
    chaine_Qmed = 'Le debit median de la periode est de : ' + str(Qmed) + ' m3/s'
    chaine_Q1 = 'Le premier quartile du boxplot pour la periode est de : ' + str(Q1) + ' m3/s'
    chaine_Q3 = 'Le troisieme quartile du boxplot pour la periode est de : ' + str(Q3) + ' m3/s'

    ####################################################################################################################
    ############################################Réalisation des graphiques##############################################
    ####################################################################################################################
    plt.clf() # nettoyer la zone graphique

    ######################### graphique des debits au cours du temps#####################

    plt.bar(date_list,debit_list,color='blue',edgecolor='blue',label='Débits journaliers')
    plt.title('Evolution des débits journaliers en m3/s en fonction du temps en jours juliens')
    plt.xlabel('Temps (jours)')
    plt.tight_layout(rect = [0, 0.1, 1, 1]) # definit des marges au graph
    plt.xticks(date_list, debit_date, rotation='vertical') # commenter l'axe x avec une liste de string
    plt.xticks(np.arange(0, len(debit_list), step=step)) # definit l'ecartement entre 2 com en axe x
    plt.ylabel('débit (m3/s)')
    plt.grid(True)
    plt.legend()
        
    plt.savefig('debit_temps_periode.png') # enregistrer la figure au format .png
    plt.clf() # nettoyer la zone graphique
    
    def clic1():
        plt.bar(date_list,debit_list,color='blue',edgecolor='blue',label='Debits journaliers')
        plt.title('Evolution des debits journaliers en m3/s en fonction du temps en jours juliens')
        plt.xlabel('Temps (jours)')
        plt.tight_layout(rect = [0, 0.1, 1, 1]) # definit des marges au graph
        plt.xticks(date_list, debit_date, rotation='vertical')# commenter l'axe x avec une liste de string
        plt.xticks(np.arange(0, len(debit_list), step=step)) # Définit l'écartement entre 2 commentaires en axe x

        plt.ylabel('Debit (m3/s)')
        plt.grid(True)
        plt.legend()
        plt.show()


    ############################# Boxplot des debits sur la periode ############################
    plt.boxplot(debit_list)
    plt.title('Répartition des débits sur la période')
    plt.grid(True)
    plt.savefig('boite_à_moustache.png')
    # plt.show()
    plt.clf() # nettoyer la zone graphique
    
    def clic2 () :
        plt.boxplot(debit_list)
        plt.title('Répartition de la population de débit sur la période')
        plt.ylabel('Débit (m3/s)')
        plt.grid(True)
        plt.show()

    ####################################################################################################################
    ############################################## LOI DE GUMBEL #######################################################
    ####################################################################################################################

    # variables et listes
    debit_list2=[]
    debit_listG=[]
    debit_listG2=[]
    rang_listG=[1]
    fhazen=[]
    uhu=[]
    ann_list=[]
    i=1900
    y=i
    e=1999
    j=1

    #liste debits sur toute la periode disponible + debits max par an
    while y<e :
        debit_list2=[]
        ann2=str(y)
        with open('Donnees.csv') as file:
            for line in file.readlines():
                line = line.split(';')
                if line[3] == ann2 :
                    debit_list2.append(float(line[5]))
        m=max(debit_list2)
        debit_listG.append(m) # liste des max par an
        rang_listG.append(j) # liste du rang
        fhazen.append((j-0.5)/(e-i)) # parametre de hazen
        uhu.append((-1)*np.log((-1)*np.log((j-0.5)/(e-i)))) # parametre u
        j=j+1
        y=y+1


    # liste annee
    while i <e:
        ann_list.append(i)
        i+= 1 


    #Debits max au cours des annee #### GRAPH ####
    plt.clf()
    plt.bar(ann_list,debit_listG,color='blue',edgecolor='blue',label='Débits max annuel')
    plt.title('Evolution des débits max par an')
    plt.xlabel('Temps (an)')
    plt.ylabel('Débit (m3/s)')
    plt.grid(True)
    plt.legend()
    plt.savefig('débit_max.png')
    #plt.show()
    plt.clf()
    
    def clic3 () :
        plt.clf()
        plt.bar(ann_list,debit_listG,color='blue',edgecolor='blue',label='Débits max annuel')
        plt.title('Evolution des débits max par an')
        plt.xlabel('Temps (an)')
        plt.ylabel('Débit (m3/s)')
        plt.grid(True)
        plt.legend()
        plt.savefig('débit_max.png')
        plt.show()

    #trie les debit max par an
    debit_listG2=sorted(debit_listG) 
    moyD=mean(debit_listG2)
    moyU=mean(uhu)

    #nuage de points
    plt.clf()
    plt.scatter(uhu,debit_listG2)
    #interpollation equation de 2nd degre
    y_param=np.polyfit(uhu,debit_listG2,2)
    y=np.poly1d(y_param) #y est lequation solution

    p=[0.5,0.8,0.9,0.95,0.98,0.99,0.995,0.998,0.999]
    uhuo=(-1)*np.log((-1)*np.log(p))
    i=0
    Qo=[]
    #liste des debits classes
    while i<len(uhuo):
        Qo.append(y(uhuo[i]))
        i=i+1
    #print(Qo) -> affichage des debits aux periodes de non retour 
    
    #reste des parametre de la courbe
    t=(np.linspace(min(uhu),max(uhu),100))
    plt.plot(t,y(t),c="grey")

    plt.title('Loi de gumbel')
    plt.xlabel('-ln(-ln(fHazen))')
    plt.ylabel('Debit m3/s')
    plt.grid(True)
    plt.savefig('gumbel.png')
    # plt.show()
    plt.clf()
    
    def clic4 () :
        #nuage de points
        plt.clf()
        plt.scatter(uhu,debit_listG)
        #interpolation equation de second degre
        y_param=np.polyfit(uhu,debit_listG,2)
        y=np.poly1d(y_param) #y est lequation solution

        p=[0.5,0.8,0.9,0.95,0.98,0.99,0.995,0.998,0.999]
        uhuo=(-1)*np.log((-1)*np.log(p))
        i=0
        Qo=[]
        #liste des debits classes
        while i<len(uhuo):
            Qo.append(y(uhuo[i]))
            i=i+1
        # print(Qo)
            
        #reste des parametre de la courbe
        t=(np.linspace(min(uhu),max(uhu),100))
        plt.plot(t,y(t),c="grey")

        plt.title('Loi de gumbel')
        plt.xlabel('-ln(-ln(fHazen))')
        plt.ylabel('Debit (m3/s)')
        plt.grid(True)
        plt.savefig('gumbel.png')
        plt.show()
    
    #actualisation affichage graphiques
    #######hydrogramme sur periode
    fr2=tk.Frame(window)
    fr2.config(width = 330 , height = 330 )

    affichage_imagebis=tk.Label(fr2,text= 'Histogramme des debits')
    affichage_imagebis.pack()

    image = Image.open('debit_temps_periode.png')
    image = image.resize((310, 310), Image.ANTIALIAS)
    img1 = ImageTk.PhotoImage(image=image)

    label=tk.Label(fr2,image=img1)
    label.pack()
    
    #bouton
    zoom1 = tk.Button (fr2,text = "zoomer",command=clic1)
    zoom1.pack()

    fr2.place(x=20,y=300)

    #######boite a moustache
    fr3=tk.Frame(window)
    fr3.config(width = 330 , height = 330 )

    affichage_imagebis=tk.Label(fr3,text= 'Repartition des debits')
    affichage_imagebis.pack()

    image2 = Image.open('boite_a_moust.png')
    image2 = image2.resize((310, 310), Image.ANTIALIAS)
    img2 = ImageTk.PhotoImage(image=image2)

    label=tk.Label(fr3,image=img2)
    label.pack()
    
    # bouton
    zoom2 = tk.Button (fr3,text = "zoomer",command=clic2)
    zoom2.pack()

    fr3.place(x=350,y=300)

    #########débit maximum par an
    fr4=tk.Frame(window)
    fr4.config(width = 330 , height = 330 )

    affichage_imagebis=tk.Label(fr4,text= 'Débit max sur l\'ensemble des donnees')
    affichage_imagebis.pack()

    image3 = Image.open('debit_max.png')
    image3 = image3.resize((310, 310), Image.ANTIALIAS)
    img3 = ImageTk.PhotoImage(image=image3)

    label=tk.Label(fr4,image=img3)
    label.pack()

    # bouton
    zoom3 = tk.Button (fr4,text = "zoomer",command=clic3)
    zoom3.pack()
    
    fr4.place(x=680,y=300)

    ########gumbel
    fr5=tk.Frame(window)
    fr5.config(width = 330 , height = 330 )

    affichage_imagebis=tk.Label(fr5,text= 'Loi de Gumbel')
    affichage_imagebis.pack()

    image4 = Image.open('gumbel.png')
    image4 = image4.resize((310, 310), Image.ANTIALIAS)
    img4 = ImageTk.PhotoImage(image=image4)

    label=tk.Label(fr5,image=img4)
    label.pack()

    #bouton
    zoom4 = tk.Button (fr5,text = "zoomer",command=clic4)
    zoom4.pack()
    
    fr5.place(x=1010,y=300)
    
    #creation chaine de caracteres dans le fichier à exporter
    annee_Non_Retour = [2,5,10,20,50,100,200,500,1000]
    chaine_Debit = 'Les débits de crue pour différentes périodes de non retour ont été determinés à partir de la loi de ' \
                   'Gumbel. Voici les résultats. '
    chaine_2 = 'Le débit de crue pour une période de non retour de ' +str(annee_Non_Retour[0]) + ' ans est de '\
               + str(Qo[0]) + ' m3/s'
    chaine_5 = 'Le débit de crue pour une période de non retour de ' +str(annee_Non_Retour[1]) + ' ans est de ' \
                                                                                                 '' + str(Qo[1]) + ' m3/s'
    chaine_10 = 'Le débit de crue pour une période de non retour de ' +str(annee_Non_Retour[2]) + ' ans est de ' \
                                                                                                  '' + str(Qo[2]) + ' m3/s'
    chaine_20 = 'Le débit de crue pour une période de non retour de ' +str(annee_Non_Retour[3]) + ' ans est de' \
                                                                                                  ' ' + str(Qo[3]) + ' m3/s'
    chaine_50 = 'Le débit de crue pour une période de non retour de ' +str(annee_Non_Retour[4]) + ' ans est de' \
                                                                                                  ' ' + str(Qo[4]) + ' m3/s'
    chaine_100 = 'Le débit de crue pour une période de non retour de ' +str(annee_Non_Retour[5]) + ' ans est de' \
                                                                                                   ' ' + str(Qo[5]) + ' m3/s'
    chaine_200 = 'Le débit de crue pour une période de non retour de ' +str(annee_Non_Retour[6]) + ' ans est de' \
                                                                                                   ' ' + str(Qo[6]) + ' m3/s'
    chaine_500 = 'Le débit de crue pour une période de non retour de ' +str(annee_Non_Retour[7]) + ' ans est de' \
                                                                                                   ' ' + str(Qo[7]) + ' m3/s'
    chaine_1000 = 'Le débit de crue pour une période de non retour de ' +str(annee_Non_Retour[8]) + ' ans est de' \
                                                                                                    ' ' + str(Qo[8]) + ' m3/s'
    #chaine_Parametre_Equation = 'Les parametres de l\'equation de Gumbel calculés sur l\'ensemble de la periode sont les suivants :'
    with open ('Rapportdanalyse.txt', 'w') as export:        # ouverture et écriture dans le fichier texte de sortie
        export.write(chaine_Qmax+'\n')
        export.write(chaine_Qmin+'\n')
        export.write(chaine_Qmoy+'\n')
        export.write(chaine_Qmed+'\n')
        export.write(chaine_Q1+'\n')
        export.write(chaine_Q3+'\n'+'\n')
        export.write(chaine_Debit+'\n'+'\n')
        export.write(chaine_2+'\n')
        export.write(chaine_5+'\n')
        export.write(chaine_10+'\n')
        export.write(chaine_20+'\n')
        export.write(chaine_50+'\n')
        export.write(chaine_100+'\n')
        export.write(chaine_200+'\n')
        export.write(chaine_500+'\n')
        export.write(chaine_1000+'\n'+'\n')
        #export.write(chaine_Parametre_Equation+'\n'+'\n')

    
    window.mainloop ()
    
########################################################################################################################
###########################creation des différents frames de l'interface graphique######################################
########################################################################################################################
window = tk.Tk ()   # creation de la fenetre principale (biblio tkinter)
#Creation de la fenetre et de son titre
window.geometry("1400x843")
window.minsize(1200, 843)
window.maxsize(1400, 843)
##bordure de la fenetre
window.iconbitmap("logo.ico")
window.title("Programme d\'analyse de données de débits")
img = tk.PhotoImage(file="cours-d'eau.png")
label = tk.Label(window, image= img)
canvas1 = tk.Canvas(window, width=1400, height=843)


canvas1.pack(fill="both", expand=True)

# Display image
canvas1.create_image(0, 0, image= img,
                     anchor="nw")

# Creation d'une barre de menu de fenetre
menu_bar = tk.Menu(window)
#Creer un premier menu
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Quitter", command = window.quit)
menu_bar.add_cascade(label="Fichier", menu = file_menu)
#configurer notre fenetre pour ajouter cette menu bar 
window.config(menu=menu_bar)



#Creation d'image gif - icone haut/droite
width = 195
height = 80
photo = tk.PhotoImage(file="UnivTours-logo.png").zoom(3).subsample(32)
canvas = tk.Canvas(window, width = width, height = height, bd = 0, highlightthickness = 0)
canvas.create_image(width/2, height/2, image = photo)
canvas.place(x=1190,y=15)

#label - titre - haut/centre
titre = tk.Label(text="Programme de rapport d\'analyse de debit", font=("Arial", 20), bg='#2DDF7A', fg='white', bd = 1)
titre.pack()

#### zone d'import
# import
nom_fich = tk.Label (text = "Donnees.csv", font=("Arial", 10), bg = '#2DDF7A', fg='white')
nom_fich.place(x=20,y=20)

############################################import des données depuis la fenêtre########################################



def clicimport():


    fichier_Import = askopenfilename(title='Selectionner votre fichier de données', filetypes=[('csv files', 'csv')])
    mon_Fichier = open(fichier_Import)
    contenu = mon_Fichier.read()

    frame_affi_parcourir = tk.Frame(window)
    frame_affi_parcourir.config(width=330, height=150)
    frame_affi_parcourir.pack_propagate(False)

    affichage_ligne = tk.Label(frame_affi_parcourir, text='Lignes du jeu de données')
    affichage_ligne.pack()

    affichage_donnees = tk.Label(frame_affi_parcourir, text=contenu, width=50,
                                 height=50)  # affiche les premières lignes du jeu de données sur la fenêtre
    affichage_donnees.pack()

    frame_affi_parcourir.place(x=20, y=50)

# Boutton "Parcourir
Parcourir = tk.Button(text="Parcourir", command=clicimport(), font=("Arial", 10))
Parcourir.place(x=140, y=20)


# état de connection du fichier
etat_fich = tk.Label(text="Fichier valide", bg='#0A4DAB', fg='#48F307')
etat_fich.place(x=220, y=20)



# ajouter les noms des présentateurs
noms = tk.Label (window, text = 'Développé par Djibril BANNE : M1 HBV 2021-2022 Univ-Tours' ,
                 font =("Arial", 9), fg ='black')
noms.place(x = 850, y = 790)

         

# configuration de l'etude
fr1=tk.Frame(window, bd = 4, relief=SUNKEN)
etat_fich = tk.Label (fr1,text = "Choisir la période sur laquelle vous souhaitez effectuer votre analyse",
                      font=("Arial", 11), fg='black', bd = 2)
etat_fich.grid (column = 0, row = 0)

# Action de selection pour le choix de la date
# ou de la durée sur laquelle on souhaite effectuer l'étude
def sel():
   if v.get()=='ans' :
    ann_d.config(state="readonly")
    ann_f.config(state="readonly")
    moiss.config(state="disabled")
   elif v.get()=='an':
    ann_d.config(state="disabled")
    ann_f.config(state="readonly")
    moiss.config(state="disabled")
   elif v.get()=='mois':
    ann_d.config(state="disabled")
    ann_f.config(state="readonly")
    moiss.config(state="readonly")
 # Readonly : Quand on peut choisir l'option
 # Disable : Désactivation de l'option

# Création des boutons pour la selection de la durée
v = tk.StringVar ()
v.set ('ans')
case1 = tk.Radiobutton (fr1,variable = v, value = 'ans',command=sel)
case2 = tk.Radiobutton (fr1,variable = v, value = 'an',command=sel)
case3 = tk.Radiobutton (fr1,variable = v, value = 'mois',command=sel)

case1.config (text = "sur plusieurs années")
case2.config (text = "sur une année")
case3.config (text = " sur un mois")
case1.grid (column = 0, row = 1)
case2.grid (column = 0, row = 2)
case3.grid (column = 0, row = 3)

label=tk.Label(fr1)

#liste des années et mois (pour la section de la période d'étude)
mois=[1,2,3,4,5,6,7,8,9,10,11,12]
ann_list=[]
i=1900
e=1999
while i <e:
    ann_list.append(i)
    i+= 1 

# Choix de l'année de départ (menu déroulant)
txt1 = tk.Label (fr1,text = "Année de depart", font=("Arial", 10), bg='#E1DADC', fg='black')
ann_d=ttk.Combobox(fr1,values=ann_list)
txt1.grid (column = 1, row = 1)
ann_d.grid (column = 1, row = 2)

# Choix de l'anné de fin
txt2 = tk.Label (fr1,text = "Année de fin", font=("Arial", 10), bg='#E1DADC', fg='black')
ann_f=ttk.Combobox(fr1,values=ann_list)
txt2.grid (column = 2, row = 1)
ann_f.grid (column = 2, row = 2)

# Choix du mois
txt3 = tk.Label (fr1,text = "Mois", font=("Arial", 10), bg='#E1DADC', fg='black')
moiss=ttk.Combobox(fr1,values=mois,state="disabled")
txt3.grid (column = 3, row = 1)
moiss.grid (column = 3, row = 2)

#bouton lancement
calculer = tk.Button (fr1,text = "calculer",command=hydro, font=("Arial", 11),bg = '#2DDF7A')
calculer.grid (column = 4, row = 3)

#placement de la frame 1 dans la fenetre
fr1.place(x=360,y=115)
# fr1.pack()

# frame pour l'import du rapport et emplacement du boutton

frame_Import = tk.Frame(window, bg = '#2DDF7A', bd = 4, relief=SUNKEN)

affichage_Texte_Import = tk.Label(frame_Import, text = 'Programme d\'analyse de données de débits',
                                  font=("Arial", 14), bg = '#2DDF7A', fg = 'black')
affichage_Texte_Import.pack()

frame_Import.place(x=600,y=25)

def importdurapport():
    fr6=tk.Frame(window, bd = 4, relief=SUNKEN)
    fr6.config(width = 150, height = 25)
    
    affichage_Texte = tk.Label(fr6, text = 'Un rapport synthétique des principales caractéristiques de la chronique '
                                           'de débit vient d\'être généré (format .txt ', font=("Arial", 11))
    affichage_Texte.pack()
    affichage_Texte2 = tk.Label(fr6, text = 'Vous le trouverez dans le même dossier que le code '
                                            'sous le nom Rapportdanalyse.txt', font=("Arial", 11))
    affichage_Texte2.pack()
    fr6.place(x=20, y=700)

# bouton
impr = tk.Button (text = "Imprimer le rapport",command= importdurapport,font=("Arial", 11),bg = '#2DDF7A')
impr.place(x=1100,y=720)


window.mainloop ()



######################################################### FIN ##########################################################


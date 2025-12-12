from django.db import migrations

def create_activity_field(apps, schema_editor):
    F = apps.get_model('association', 'ActivityField')
    G = apps.get_model('association', 'ActivityFieldGroup')
    # clean
    F.objects.all().delete()
    G.objects.all().delete()
    # build activity fields
    [
            F.objects.create(
                name=f,
                activity_field_group=G.objects.get_or_create(name=g)[0]
            )
            for g, lf in [
                    [
                        "Culture", [
                            "Association culturelle ou artistique (musique, danse photographie, théâtre, lecture, écriture, arts plastiques…) y compris enseignement d’activités culturelles",
                            "MJC, centre d’action culturelle, club culturel",
                            "Spectacle vivant (création, production, prestation de soutien, conseils, gestion administrative…)",
                            "Gestion de salles de spectacles",
                            "Association de défense et/ou de gestion du patrimoine culturel et historique : protection, valorisation, étude du patrimoine, attractions touristiques culturelles",
                            "Bibliothèque, musée, médiathèque, ludothèque…",
                            "Échanges culturels internationaux",
                            "Autre activité culturelle ou artistique",
                        ]
                    ],[
                        "Sports", [
                            "Club de sport, enseignement des disciplines sportives, ligue ou fédération sportives",
                            "Gestion d’installations sportives et autres activités liées au sport",
                            "Chasse et pêche",
                            "Autre association orientée vers le sport",
                        ],
                    ],[
                        "Loisirs et vie sociale", [
                            "Scoutisme ou autres association de loisirs pour les jeunes",
                            "Centre aéré associatif",
                            "Club du 3ème âge ou autre association de loisirs pour les personnes âgées",
                            "Comité des fêtes",
                            "Association de retraités ou de personnels d’une entreprise ou d’une administration",
                            "Association de quartier ou locale, amicale ou groupement de personnes originaires d’une même région ou d’un même pays",
                            "Tourisme social (hébergement, restauration)",
                            "Autre association de loisir",
                        ],
                    ],[
                        "Action sociale (avec ou sans hébergement), action humanitaire ou caritative", [
                            "Association familiale, de soutien aux familles, à des mères de famille isolées, d’aide à l’enfance",
                            "Aide à l’insertion sociale et professionnelle, aide à l’emploi, (jeunes ou adultes en difficulté, chômeurs de longue durée, etc.)",
                            "Aide pour le travail des personnes handicapées",
                            "Accueil de jeunes enfants",
                            "Accueil et/ou hébergement d’enfants en difficulté",
                            "Accueil et/ou hébergement (médicalisé ou non) de personnes handicapées (enfants, adultes…)",
                            "Hébergement (médicalisé ou non) pour personnes âgées, dont EHPAD",
                            "Aide au logement",
                            "Foyers de jeunes travailleurs",
                            "Aide à domicile",
                            "Aide aux migrants",
                            "Association caritative ou à but humanitaire (y compris aide internationale)",
                            "Autre association d’action sociale",
                        ],
                    ],[
                        "Santé", [
                            "Association dispensant des soins (activités hospitalières, soins de médecine générale ou spécialisée, soins infirmiers ou de rééducation…)",
                            "Association d’aide aux malades (visites à l’hôpital, prêt de matériel médical, etc.) ou à leurs proches",
                            "Groupement de malades",
                            "Recherche médicale",
                            "Autre association de santé",
                        ],
                    ],[
                        "Enseignement, formation, recherche", [
                            "Enseignement primaire ou secondaire (technique, professionnel ou général)",
                            "Enseignement supérieur",
                            "Formation continue d’adultes",
                            "Recherche hors recherche médicale",
                            "Autre activité d’enseignement (hors enseignement culturel, artistique ou sportif)",
                        ],
                    ],[
                        "Défense de droits, de causes ou d’intérêts", [
                            "Association de parents d’élèves",
                            "Association d’élèves, d’étudiants, d’anciens élèves ou étudiants",
                            "Association patriotique ou d’anciens combattants",
                            "Association cultuelle, religieuse ou paroissiale",
                            "Organisation politique, club ou cercle de réflexion",
                            "Protection de l’environnement, des animaux, de la flore et de la faune, gestion de jardins, parcs ou réserves",
                            "Défense des consommateurs, des usagers de services publics",
                            "Groupement professionnel ou syndical",
                            "Association de locataires ou de propriétaires",
                            "Association de défense des droits humains, des droits des femmes, de minorités",
                            "Autre association de défense de causes, de droits et d’intérêts",
                        ],
                    ],[
                        "Développement local et gestion de services économiques", [
                            "Association de développement économique et de développement local (y compris organisation de circuits courts type AMAP)",
                        ],
                    ],
            ]
            for f in lf
    ]


class Migration(migrations.Migration):

    dependencies = [
        ('association', '0001_initial'),
    ]

    operations = [
            migrations.RunPython(create_activity_field),
    ]

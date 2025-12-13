from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn import linear_model
from cv2 import imread, imshow, rectangle, putText, waitKey, destroyAllWindows, FONT_HERSHEY_SIMPLEX


class machinelearning:

    def retirer_valeurs_nulles(tableau):
        return tableau.dropna()

    def separation_entrainement_test(X,y,test_percentage):
        X_train, X_test, y_train, y_test = train_test_split(X,y,test_size = test_percentage)
        return X_train, X_test, y_train, y_test

    def rapport_de_classification(vraie_val, prediction):
        return classification_report(vraie_val, prediction)

    def matrice_de_confusion(vraie_val, prediction):
        return confusion_matrix(vraie_val, prediction)

    def affichage_matrice(mat_confusion, labels):
        cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = mat_confusion, display_labels = labels)
        return cm_display

    def score_de_precision(vraie_val, prediction):
        return accuracy_score(vraie_val, prediction)

    def regression_lineaire(ordre):
        return linear_model.LinearRegression()

    def arbre_de_decision(profondeur):
        return DecisionTreeClassifier(max_depth=profondeur)

    def foret_aleatoire(estimateurs):
        return RandomForestClassifier(n_estimators=estimateurs, max_depth = 5)

    def reseau_de_neurones(couches_cachees):
        return MLPClassifier(hidden_layer_sizes=couches_cachees)

    def lecture_image(nom_image):
        return imread(nom_image)

    def afficher_image(nom_fenetre, image):
        return imshow(nom_fenetre, image)

    def ajouter_rectangle(image, point_bas_gauche, point_haut_droite, couleur):
        return rectangle(image, point_bas_gauche, point_haut_droite, couleur, 2)

    def ajouter_text(image, texte, point_bas_gauche, couleur):
        return putText(image, texte, (point_bas_gauche[0], point_bas_gauche[1]-10), FONT_HERSHEY_SIMPLEX, 0.6, couleur, 2)

    def attendre(nombre):
        return waitKey(0)

    def supprimer_fenetre(self):
        destroyAllWindows()
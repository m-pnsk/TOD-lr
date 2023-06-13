from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score
import joblib

# Крок 1: Завантаження датасету та поділ на тренувальну та тестову вибірки
breast_cancer = load_breast_cancer()
X_train, X_test, y_train, y_test = train_test_split(breast_cancer.data, breast_cancer.target,
                                                    test_size=0.2, random_state=42)

# Крок 2: Створення пайплайну
pipeline = Pipeline([
    ('scaler', StandardScaler()),  # Передобробка даних - масштабування
    ('pca', PCA()),  # Відбір ознак - PCA
    ('regressor', LinearRegression())  # Лінійна регресія
])

# Крок 3: Визначення гіперпараметрів для налаштування
parameters = {
    'pca__n_components': [2, 3],  # Кількість головних компонент для PCA
    'regressor__fit_intercept': [True, False]  # Параметр fit_intercept для LinearRegression
}

# Крок 4: Використання GridSearchCV для налаштування гіперпараметрів та відбору ознак
grid_search = GridSearchCV(pipeline, parameters, scoring='r2', cv=5)
grid_search.fit(X_train, y_train)

# Крок 5: Оцінка якості пайплайну на тестовій вибірці
y_pred = grid_search.predict(X_test)
r2 = r2_score(y_test, y_pred)
print(f'R2 Score: {r2:.2f}')

# Крок 6: Оцінка базової моделі, яка не використовує пайплайн
base_model = LinearRegression()
base_model.fit(X_train, y_train)
base_y_pred = base_model.predict(X_test)
base_r2 = r2_score(y_test, base_y_pred)
print('--- Base Model ---')
print(f'R2 Score: {base_r2:.2f}')

# Крок 7: Збереження навченого пайплайну для подальшого використання
joblib.dump(grid_search, 'pipeline.pkl')

# Завантаження збереженого пайплайну
loaded_pipeline = joblib.load('pipeline.pkl')

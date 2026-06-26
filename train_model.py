import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

df = pd.read_excel("agrisense_1000_records.xlsx")

X = df[[
"SoilMoisture","Temperature","Humidity","Rainfall",
"pH","Nitrogen","Phosphorus","Potassium",
"WindSpeed","UV"
]]

le = LabelEncoder()
y = le.fit_transform(df["Irrigation"])

X_train,X_test,y_train,y_test = train_test_split(
    X,y,test_size=0.2,random_state=42
)

model = RandomForestClassifier(
    n_estimators=300,
    max_depth=12,
    random_state=42
)

model.fit(X_train,y_train)

pickle.dump(model, open("model.pkl","wb"))

print("✅ Model trained & saved")
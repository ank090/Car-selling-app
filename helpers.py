import pandas as pd
from models import Models

class FeatureExtraction:

    @classmethod
    def extract_brand(cls,df):
        """
        Extracts the name of the brand of the car from the name of the car.
        """
        df['Brand'] = df['Name'].str.capitalize().apply(lambda x: x.split()[0])
        return df
    
    @classmethod
    def remove_useless_column(cls,df):
        """
        Removes the columns that are not important for the prediction.
        NOTE: Must be used only after extract_brand.
        """
        if 'Unnamed: 0' in df.columns:
            df.drop(columns=['Unnamed: 0'], inplace=True)
        df.drop(columns=['Name'], inplace=True)
        df.drop(columns=['New_Price'], inplace=True)
        return df
    
    @classmethod
    def map_nuumeric_owner(cls,df):
        """
        Assign numeric values to the no of owners the car had.
        """
        owner = {'First':1, 'Second':2, 'Fourth & Above':4, 'Third':3}
        df['Owner_Type'] = df['Owner_Type'].apply(lambda x:owner[x])
        return df

    @classmethod
    def remove_units(cls,df):
        """
        Remove the unit of measurements from the columns for converting it to numeric data.
        NOTE: Must be ran before change_data_to_numeric method.
        """
        df['Mileage'] = df['Mileage'].str.replace('kmpl', '').str.replace('km/kg', '')
        df['Engine'] = df['Engine'].str.replace('CC', '')
        df['Power'] = df['Power'].str.replace('bhp', '')
        return df

    @classmethod
    def change_data_to_numeric(cls,df):
        """
        Covert object data to numeric data
        """
        df['Mileage'] = pd.to_numeric(df['Mileage'], errors='coerce')
        df['Engine'] = pd.to_numeric(df['Engine'], errors='coerce')
        df['Power'] = pd.to_numeric(df['Power'], errors='coerce')
        return df
    
    @classmethod
    def handle_null_values(cls,df):
        """
        Handles null values by either removing row or by filling it with valid data.
        NOTE: Must be ran before any other function in the class. 
        """
        df.dropna(subset = ['Name', 'Kilometers_Driven'], inplace=True)
        df['Fuel_Type'] = df['Fuel_Type'].fillna('Petrol')
        df['Transmission'] = df['Transmission'].fillna('Manual')
        df['Owner_Type'] = df['Owner_Type'].fillna(1)
        df['Year'] = df['Year'].fillna(2014)
        df['Location'] = df['Location'].fillna('Mumbai')
        df['Mileage'] = df['Mileage'].fillna(df['Mileage'].mean())
        df['Engine'] = df['Engine'].fillna(df['Engine'].mean())
        df['Power'] = df['Power'].fillna(df['Power'].mean())
        df['Seats'] = df['Seats'].fillna(df['Seats'].mean())
        return df

class Features:
    def __init__(self):
        self.extractor = FeatureExtraction()
    
    def extract_bulk(self, df):
        """
        Extract all the relavent data from dataset and prepare it to feed to the models.
        """
        df = self.extractor.remove_units(df)
        df = self.extractor.change_data_to_numeric(df)        
        df = self.extractor.handle_null_values(df)
        df = self.extractor.extract_brand(df)
        df = self.extractor.remove_useless_column(df)
        df = self.extractor.map_nuumeric_owner(df)
        #print(df.columns)
        return df
    
    def extract(self,df):
        """
        Extracts all the relavent data from request and prepare it to be fed to the models.
        """
        df = self.extractor.remove_units(df)
        df = self.extractor.change_data_to_numeric(df)
        df = self.extractor.extract_brand(df)
        df = self.extractor.remove_useless_column(df)
        df = self.extractor.map_nuumeric_owner(df)
        return df

class Prediction:
    def __init__(self) -> None:
        self.models = Models()
        self.extractor = Features()
    
    def encode_predict(self,data):
        """
        Handles encoding and predicting the price based on the encoded values.
        """
        engineered_data = self.models.encoder.transform(data)
        pred = self.models.regression_model.predict(engineered_data)*100000 # to convert price in Lakh
        pred = list(map(lambda x:round(x), pred))
        prediction = pd.DataFrame(pred, columns=['Predicted Price'])
        return prediction

    def input_validator(func):
        """
        Handles validation of input parameters against parameters need by the models.
        """
        cols = {'Name', 'Location', 'Year', 'Kilometers_Driven',
       'Fuel_Type', 'Transmission', 'Owner_Type', 'Mileage', 'Engine', 'Power',
       'Seats', 'New_Price'}
        def check(*args):
            if not set(cols).issubset(set(args[1].columns)):
                diff = cols.difference(set(args[1].columns))
                raise KeyError("Columns",diff,"needed for model, are not present in the data passed.")
            return func(*args)
        return check
    
    @input_validator    
    def make_bulk_prediction(self, data):
        """
        Handles extraction of data and making prediction for bulk dataset.
        """
        engineered_data = self.extractor.extract_bulk(data)
        prediction = self.encode_predict(data=engineered_data)
        return prediction
    @input_validator
    def make_prediction(self, data):
        """
        Handles extraction of data and making prediction for a single dataset.
        """
        engineered_data = self.extractor.extract(data)
        prediction = self.encode_predict(data=engineered_data)
        return prediction
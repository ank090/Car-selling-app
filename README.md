# Car Becho App

# API Documentation

## Overview
This document provides details on the available endpoints for the car price prediction service. The service supports two primary endpoints: `price_predictor` and `bulk_price_predictor`. Both endpoints allow users to predict car prices based on provided input data.

## Endpoints
### 2. `/price_predictor`
**Description:** This endpoint accepts form data for a single car record and returns the predicted price for the car.

**Method:** POST

**Request:**
- **Headers:**
  - `Content-Type: application/x-www-form-urlencoded
- **Body:**
    - `Name`
    - `Location`
    - `Year`
    - `Kilometers_Driven`
    - `Fuel_Type`
    - `Transmission`
    - `Owner_Type`
    - `Mileage`
    - `Engine`
    - `Power`
    - `Seats`
    - `New_Price`

### 1. `bulk_price_preditor`
**Description:** This endpoint accepts a CSV file containing multiple records of car details and returns predicted prices for each record.

**Method:** POST

**Request:**
- **Headers:**
  - `Content-Type: multipart/form-data`
- **Body:**
  - A `.csv` file with the following columns:
    - `Name`
    - `Location`
    - `Year`
    - `Kilometers_Driven`
    - `Fuel_Type`
    - `Transmission`
    - `Owner_Type`
    - `Mileage`
    - `Engine`
    - `Power`
    - `Seats`
    - `New_Price`

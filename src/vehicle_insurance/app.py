from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.vehicle_insurance.pipeline.prediction import (
    VehicleData,
    PredictionPipeline
)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="vehicledata.html",
        context={}
    )


@app.post("/predict", response_class=HTMLResponse)
async def predict(
    request: Request,

    Gender: str = Form(...),
    Age: int = Form(...),
    Driving_License: int = Form(...),
    Region_Code: float = Form(...),
    Previously_Insured: int = Form(...),
    Vehicle_Age: str = Form(...),
    Vehicle_Damage: str = Form(...),
    Annual_Premium: float = Form(...),
    Policy_Sales_Channel: float = Form(...),
    Vintage: int = Form(...)
):

    try:

        vehicle_data = VehicleData(
            Gender=Gender,
            Age=Age,
            Driving_License=Driving_License,
            Region_Code=Region_Code,
            Previously_Insured=Previously_Insured,
            Vehicle_Age=Vehicle_Age,
            Vehicle_Damage=Vehicle_Damage,
            Annual_Premium=Annual_Premium,
            Policy_Sales_Channel=Policy_Sales_Channel,
            Vintage=Vintage
        )

        df = vehicle_data.get_dataframe()

        pipeline = PredictionPipeline()

        prediction = pipeline.predict(df)

        result = (
            "Customer Interested"
            if prediction == 1
            else "Customer Not Interested"
        )

        return templates.TemplateResponse(
            request=request,
            name="vehicledata.html",
            context={
                "prediction_text": result,

                "Gender": Gender,
                "Age": Age,
                "Driving_License": Driving_License,
                "Region_Code": Region_Code,
                "Previously_Insured": Previously_Insured,
                "Vehicle_Age": Vehicle_Age,
                "Vehicle_Damage": Vehicle_Damage,
                "Annual_Premium": Annual_Premium,
                "Policy_Sales_Channel": Policy_Sales_Channel,
                "Vintage": Vintage
            }
        )

    except Exception as e:

        return templates.TemplateResponse(
            request=request,
            name="vehicledata.html",
            context={
                "prediction_text": f"Error: {e}",

                "Gender": Gender,
                "Age": Age,
                "Driving_License": Driving_License,
                "Region_Code": Region_Code,
                "Previously_Insured": Previously_Insured,
                "Vehicle_Age": Vehicle_Age,
                "Vehicle_Damage": Vehicle_Damage,
                "Annual_Premium": Annual_Premium,
                "Policy_Sales_Channel": Policy_Sales_Channel,
                "Vintage": Vintage
            }
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.vehicle_insurance.app:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
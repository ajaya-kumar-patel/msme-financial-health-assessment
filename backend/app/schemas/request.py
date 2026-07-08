from pydantic import BaseModel

class PredictionRequest(BaseModel):
    Business_Size: str
    Business_Age: float
    Industry_Type: str
    Entity_Type: str
    Monthly_GST_Sales: float
    GST_Growth_Rate: float
    GST_Filing_Delay: float
    GST_Compliance_Rate: float
    Monthly_UPI_Count: int
    Monthly_UPI_Value: float
    Digital_Sales_Ratio: float
    Average_Bank_Balance: float
    Monthly_Credit: float
    Monthly_Debit: float
    Cashflow_Volatility: float
    Employee_Count: int
    Payroll_Consistency: float
    Vendor_Payment_Delay: float
    Working_Capital_Cycle: float
    EMI_Bounce_Count: int
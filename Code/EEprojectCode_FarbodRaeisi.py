import numpy as np
import numpy_financial as npf
import matplotlib.pyplot as plt

def F_from_P(present_value, interest_rate, years):
    future_value = present_value * (1 + interest_rate) ** years
    return future_value

def F_from_A(annual_cash_flow, interest_rate, years):

    future_value = annual_cash_flow * ((1 + interest_rate)**years - 1) / interest_rate
    return future_value

def A_from_P(present_worth, interest_rate, years):
    eacf = (interest_rate * present_worth) / (1 - (1 + interest_rate)**-years)
    return eacf

def P_from_A(equivalent_annual_cash_flow, interest_rate, years):
    pw = equivalent_annual_cash_flow * ((1 - (1 + interest_rate)**-years) / interest_rate)
    return pw

def P_from_F(future_value, interest_rate, years):
    pw = future_value / ((1 + interest_rate) ** years)
    return pw

def A_from_F(future_value, interest_rate, years):

    eacf = future_value * interest_rate / ((1 + interest_rate)**years - 1)
    return eacf

def depreciation(present_worth, SV, n):
    depreciation = (present_worth - SV) / n;
    return depreciation


def calculate_economic_metrics(pw, fw, ai, sv, ir, tr, n, dep_rate):
    net_annual_income = ai * (1 - tr)
    annual_tax_saving = dep_rate * tr
    net_annual_cash_flow = net_annual_income + annual_tax_saving
    cash_flows = [-pw] + [net_annual_cash_flow] * (n - 1) + [net_annual_cash_flow + sv + A_from_F(fw, ir, n)]
    
    npv = npf.npv(ir, cash_flows)
    
    irr = npf.irr(cash_flows)
    
    cumulative_cash_flows = np.cumsum(cash_flows)
    payback_period = np.argmax(cumulative_cash_flows >= 0)
    
    is_economical = npv > 0 and irr > ir and payback_period < n
    
    metrics = {
        'NPV': npv,
        'IRR': irr,
        'Payback Period': payback_period,
        'Is Economical': is_economical
    }
    
    return metrics, cash_flows, cumulative_cash_flows

def plot_cash_flows(cash_flows, cumulative_cash_flows, n):
    years = np.arange(0, n + 1)
    
    plt.figure(figsize=(12, 6))
    
    plt.subplot(2, 1, 1)
    plt.bar(years, cash_flows, color='blue', alpha=0.7)
    plt.xlabel('Year')
    plt.ylabel('Annual Cash Flow')
    plt.title('Annual Cash Flow Over Time')
    
    plt.subplot(2, 1, 2)
    plt.plot(years, cumulative_cash_flows, color='green', marker='o')
    plt.xlabel('Year')
    plt.ylabel('Cumulative Cash Flow')
    plt.title('Cumulative Cash Flow Over Time')
    
    plt.tight_layout()
    plt.show()

def Start1():
    quest = input('please choose:F_from_P(1), F_from_A(2), P_from_A(3), P_from_F(4), A_from_P(5), A_from_F(6)')
    interest_rate = int(input('how much is the anuual rate?'))
    n = int(input('project lifetime?(in years)'))
    
    
    if quest == '1':
        present_worth = int(input('what is your present worth?(P)'))
        F = F_from_P(present_worth, interest_rate, n)
        print('F is equal to ', F);
        
    elif quest == '2':
        annual_income = int(input('How much is your projects annual income?(A)'))
        F = F_from_A(annual_income, interest_rate, n)
        print('F is equal to ', F);
        
        
        
    elif quest == '3':
        annual_income = int(input('How much is your projects annual income?(A)'))
        P = P_from_A(annual_income, interest_rate, n)
        print('P is equal to ', P);
        
        
    elif quest == '4' :
        future_worth = int(input('what is your future worth?(F)'))
        P = P_from_F(future_worth, interest_rate, n)
        print('P is equal to ', P);
        
        
    elif quest == '5' :
        present_worth = int(input('what is your present worth?(P)'))
        A = A_from_P(present_worth, interest_rate, n)
        print('A is equal to ', A);
        
        
    elif quest == '6' :
        future_worth = input('what is your future worth?(F)')
        A = A_from_F(future_worth, interest_rate, n)
        print('A is equal to ', A);
        
        
def Start2():
    present_worth = float(input('what is your present worth?(P)'))
    future_worth = float(input('what is your future worth?(F)'))
    annual_income = float(input('what is your projects annual income?(A)'))
    salvage_value = float(input('SV?'))
    interest_rate = float(input('how much is the anuual rate?'))
    tax_rate = float(input('how much is the tax rate?'))
    n = int(input('project lifetime?(in years)'))
    depreciation_rate = depreciation(present_worth, salvage_value, n)  # Straight-line depreciation rate
    
    metrics, cash_flows, cumulative_cash_flows = calculate_economic_metrics(
        present_worth, future_worth, annual_income, salvage_value, interest_rate, tax_rate, n , depreciation_rate
        )

    print(f"NPV: ${metrics['NPV']:.2f}")
    print(f"IRR: {metrics['IRR']*100:.2f}%")
    print(f"Payback Period: {metrics['Payback Period']} years")
    print(f"Is the project economical? {'Yes' if metrics['Is Economical'] else 'No'}")
    
    plot_cash_flows(cash_flows, cumulative_cash_flows, n)
# Start
print('Thanks for Choosing This App, This app can tell weather your project is economical(1) or convert parameters such as A, P and F to each other(2)')
service = input('Please choose your required service: ')
if service == '1':
    Start1()
if service == '2':
    Start2()
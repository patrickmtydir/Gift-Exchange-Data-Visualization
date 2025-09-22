import seaborn as sb
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
import numpy as np
import math
from linearmodels.panel import PanelOLS
from scipy.stats import norm, ranksums
import builtins
control_data=pd.DataFrame()
treatment_data=pd.DataFrame()
all_data=pd.DataFrame()
summary_stats=pd.DataFrame()

#Importing Data into dataframes and creating session and treatment variables
for treatment in ["Effort Before", "Effort After"]: #, "Binary Effort"
    for session in list(range(1,8)):
        file_path=f"{treatment}/Session {session}"
        data= pd.read_excel(file_path+"/Transactions.xlsx")
        data["session"]=f"{session}"
        if treatment == "Effort Before":
            data["treatment"]=0
            control_data=pd.concat([control_data,data])
            all_data=pd.concat([all_data,data])
        if treatment == "Effort After":
            data["treatment"]=1
            treatment_data=pd.concat([treatment_data,data])
            all_data=pd.concat([all_data,data])        

        # Variable for naming graphs
        session_title=f"{treatment} "+ f"{session}:"

        #Mean Effort By Wage Graph
        mean_effort_per_wage=data.groupby("wage")["effort"].mean()
        mean_effort_per_wage.reset_index(level="wage")
        plt.title("Average Effort vs. Wage - "+session_title)
        plt.xlim([29, 130])
        plt.ylim([0, 1])
        plt.xticks([30,50,70,90,110,130])
        sb.scatterplot(mean_effort_per_wage, color="red")
        sb.regplot(data=mean_effort_per_wage, x=mean_effort_per_wage.index, y=mean_effort_per_wage,ci=0, scatter_kws={"color": "black"}, line_kws={"color": "red"})
        plt.plot([], [], color='blue', label='estimated effort')
        plt.legend(["estimated effort","average observed effort"])
        plt.xlabel("Wage")
        plt.ylabel("Average Effort")
        plt.savefig(file_path+"/Average Effort Per Wage "+f"{treatment} "+f"{session}"+".png")
        plt.clf()

        #Jitterplot
        ax=plt.gca()
        plt.title("Effort vs. Wage Jitterplot - "+session_title)
        jittered_x = data["wage"] + np.random.uniform(-0.3, 0.3, size=len(data))
        ax.scatter(jittered_x, data["effort"], color="black", alpha=0.6)
        sb.regplot(data=data, x="wage", y="effort", ax=ax, scatter=False, color='red', ci=None)
        plt.xlabel("Wage")
        plt.ylabel("Effort")
        plt.savefig(file_path+"/Effort Per Wage Jitterplot"+" "+f"{treatment} "+f"{session}"+".png")
        plt.clf()

        # Wages over time graph
        plt.title("Evolution of Wages Over Time - "+session_title)
        data["fixed_round"]=data["round_number"]-1
        data["round_number_plotting"]=data["fixed_round"]+(data["transaction_number"]/4)
        plt.xticks([1,2,3,4,5,6,7,8,9,10,11,12])
        sb.scatterplot(data=data, x=data["round_number_plotting"], y=data["wage"],color="black")
        plt.xlabel("Round Number")
        plt.ylabel("Wage")
        plt.savefig(file_path+"/Wage Offers Over Time"+" "+f"{treatment} "+f"{session}"+".png")
        plt.clf()

        # Wage vs Effort Recieved in Previous Round
        ax=plt.gca()
        plt.title("Wage vs. Effort Recieved in Previous Round - "+session_title)
        wage_vs_effort_before_list=[]
        for row in range(len(data)):
            round_number_row=data.iloc[row]
            round_number=round_number_row["round_number"]
            session_number=round_number_row["session"]
            if round_number >1:
                firm_id=round_number_row["firm_id"]
                wage_offered=round_number_row["wage"]
                previous_round=round_number-1
                effort_recieved_row=data.loc[(data["round_number"]==previous_round) & (data["firm_id"]==firm_id) & (data["session"]==session_number),"effort"]
                if len(effort_recieved_row)>0:
                    effort_recieved=effort_recieved_row.item()
                    wage_vs_effort_before_list.append({"round_number":round_number, "firm_id":firm_id, "effort_recieved":effort_recieved, "wage_offered":wage_offered})
        wage_vs_effort_before_data=pd.DataFrame(wage_vs_effort_before_list)   
        sb.scatterplot(data=wage_vs_effort_before_data, x=wage_vs_effort_before_data["effort_recieved"], y=wage_vs_effort_before_data["wage_offered"], ax=ax, color="black", alpha=0.6)
        sb.regplot(data=wage_vs_effort_before_data, x=wage_vs_effort_before_data["effort_recieved"], y=wage_vs_effort_before_data["wage_offered"], ax=ax, scatter=False, color='red', ci=None)
        #sb.stripplot(data=wage_vs_effort_before_data, x=wage_vs_effort_before_data["effort_recieved"], y=wage_vs_effort_before_data["wage_offered"], jitter=True, color="black", alpha=0.6)
        plt.xlabel("Effort Recieved in Round t")
        plt.ylabel("Wage offered in Round t+1")
        plt.savefig(file_path+"/Wage vs. Effort Recieved in Previous Round"+" "+f"{treatment} "+f"{session}"+".png")
        plt.clf()

        # Wage vs Surplus Recieved in Previous Round
        ax=plt.gca()
        plt.title("Wage vs. Surplus Recieved in Previous Round - "+session_title)
        wage_vs_surplus_before_list=[]
        for row in range(len(data)):
            round_number_row=data.iloc[row]
            round_number=round_number_row["round_number"]
            session_number=round_number_row["session"]
            if round_number >1:
                firm_id=round_number_row["firm_id"]
                wage_offered=round_number_row["wage"]
                previous_round=round_number-1
                surplus_recieved_row=data.loc[(data["round_number"]==previous_round) & (data["firm_id"]==firm_id) & (data["session"]==session_number),"firm_surplus"]
                if len(surplus_recieved_row)>0:
                    surplus_recieved=surplus_recieved_row.item()
                    wage_vs_surplus_before_list.append({"round_number":round_number, "firm_id":firm_id, "surplus_recieved":surplus_recieved, "wage_offered":wage_offered})
        wage_vs_surplus_before_data=pd.DataFrame(wage_vs_surplus_before_list)
        sb.scatterplot(data=wage_vs_surplus_before_data, x=wage_vs_surplus_before_data["surplus_recieved"], y=wage_vs_surplus_before_data["wage_offered"], ax=ax, color="black", alpha=0.6)
        sb.regplot(data=wage_vs_surplus_before_data, x=wage_vs_surplus_before_data["surplus_recieved"], y=wage_vs_surplus_before_data["wage_offered"], ax=ax, scatter=False, color='red', ci=None)
        #sb.stripplot(data=wage_vs_surplus_before_data, x=wage_vs_surplus_before_data["surplus_recieved"], y=wage_vs_surplus_before_data["wage_offered"], jitter=True, color="black", alpha=0.6)
        plt.xticks([10,20,30,40,50,60,70,80,90])
        plt.xlabel("Surplus Recieved in Round t")
        plt.ylabel("Wage offered in Round t+1")
        plt.savefig(file_path+"/Wage vs. Surplus Recieved in Previous Round"+" "+f"{treatment} "+f"{session}"+".png")
        plt.clf()

        # Summary Statistics
        data["total_surplus"]=data["worker_surplus"]+data["firm_surplus"]
        data["firm_surplus_share"]=data["firm_surplus"]/data["total_surplus"]
        Averages=data.groupby("session").mean()
        Averages["session"]=f"{session}"
        Averages["treatment"]=f"{treatment}"
        columns=['wage',"effort","worker_surplus","firm_surplus","total_surplus", "firm_surplus_share","session","treatment"]
        Averages.to_csv(file_path+"/Summary Statistics.csv", columns=columns, index=False)
        summary_stats=pd.concat([summary_stats,Averages])

        # Summary Table
        mean_wage_groups=data.groupby(pd.cut(data['wage'], [29, 44, 59, 74, 89, 104, 126])).mean().round(2)
        med_wage_groups=data.groupby(pd.cut(data['wage'], [29, 44, 59, 74, 89, 104, 126])).median().round(2)
        count_wage_groups=data.groupby(pd.cut(data['wage'], [29, 44, 59, 74, 89, 104, 126])).count()
        table_data={"Average Observed Effort Level":mean_wage_groups["effort"], "Median Observed Effort Level":med_wage_groups["effort"], "n":count_wage_groups["firm_id"]}
        table_dataframe=pd.DataFrame(table_data)
        custom_labels = ["30 to 44", "45 to 59", "60 to 74", "75 to 89", "90 to 104", "105 to 125"]
        table_dataframe = table_dataframe.fillna("-")
        table_dataframe.index = custom_labels
        table_dataframe.index.name = "Wage Range"
        table_dataframe["Average Observed Effort Level"]=table_dataframe["Average Observed Effort Level"].astype(str)
        table_dataframe["Median Observed Effort Level"]=table_dataframe["Median Observed Effort Level"].astype(str)
        str = builtins.str
        with open(file_path+"/Session Summary Table"+" "+f"{treatment} "+f"{session}"+"table.tex","w") as f:
            f.write(table_dataframe.to_latex(index=True, column_format="cccc", multirow=False))
    # End of session loop
    session_title=f"{treatment}+ Aggregated:"
    file_path=f"{treatment}/"
    
    # Treatment Differences and Stats

# End of treatment loop

# Aggregate Differences and Stats

# Summary Statistics
summary_stats.to_csv("Aggregated Summary Statistics.csv", columns=columns, index=False)

# Mean Observed Effort Graph
copy_data=all_data.copy(deep=False)
copy_data["treatment"]=copy_data["treatment"].replace({0:"Effort After", 1:"Effort Before"})
copy_data.rename(columns={'treatment': 'Treatment'}, inplace=True)
grouped_data=copy_data.groupby(["wage","session","Treatment"]).mean()
grouped_data_means=copy_data.groupby(["wage","Treatment"]).mean()
grouped_data_means=grouped_data_means.reset_index()

# Plot over average of sessions
ax=sb.lmplot(data=grouped_data_means, x="wage",y="effort", hue="Treatment", ci=0, palette="colorblind", fit_reg=True, legend=True)
ax.set(xlabel="Wage",ylabel="Average Effort", title="Aggregated Average Effort Per Wage", xticks=[30,50,70,90,110,130], yticks=[0,0.2,0.4,0.6,0.8,1])
ax.savefig("Aggregated Average Effort Per Wage", bbox_inches="tight")
plt.clf()

# Wages over time graph
data_round_fixed=copy_data
data_round_fixed["round_number"]=data_round_fixed["round_number"]-1
data_round_fixed["round_number_plotting"]=data_round_fixed["round_number"]+(data_round_fixed["transaction_number"]/4)
ax=sb.lmplot(data=data_round_fixed, x="round_number_plotting", y="wage", x_jitter=0.1, y_jitter=0.1, hue="Treatment", palette="colorblind", scatter_kws={'alpha': 0.25}, ci=0, fit_reg=True, legend=False)
ax.set(xlabel="Round Number",ylabel="Wage", title="Evolution of Wages Over Time", xticks=[1,2,3,4,5,6,7,8,9,10,11,12], yticks=[30,50,70,90,110,130])
plt.legend(bbox_to_anchor=(1.0, 0.9), loc='upper right')
ax.figure.savefig("Aggregated Offers Over Time.png", bbox_inches="tight")
plt.clf()

# Effort over time graph
ax=sb.lmplot(data=data_round_fixed, x="round_number_plotting", y="effort", x_jitter=0.1, y_jitter=0.1, hue="Treatment", palette="colorblind", scatter_kws={'alpha': 0.25}, ci=0, fit_reg=True, legend=False)
ax.set(xlabel="Round Number",ylabel="Effort", title="Evolution of Effort Over Time", xticks=[1,2,3,4,5,6,7,8,9,10,11,12], yticks=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0])
plt.legend(bbox_to_anchor=(1.0, 0.9), loc='upper right')
ax.figure.savefig("Aggregated Effort Levels Over Time.png", bbox_inches="tight")
plt.clf()

#Jitterplot
ax=sb.lmplot(data=data_round_fixed, x="wage", y="effort", x_jitter=0.05, y_jitter=0.05, hue="Treatment", scatter_kws={'alpha': 0.3}, ci=0, fit_reg=True, legend=False)
ax.set(xlabel="Wage",ylabel="Effort", title="Aggregate Effort vs. Wage", xticks=[30,50,70,90,110,130], yticks=[0,0.2,0.4,0.6,0.8,1])
plt.legend(bbox_to_anchor=(0.65, 1), loc='upper left')
plt.savefig("Aggregate Effort vs. Wage Jitter.png", bbox_inches="tight")
plt.clf()

# Basic OLS with no fixed effects
control_data["const"]=1
treatment_data["const"]=1

control_data["session_dummy"]=control_data["session"]
control_data=pd.get_dummies(control_data, columns=["session_dummy"])
control_data["worker_identification"]=control_data["session"].astype(str)+"_"+control_data["worker_id"].astype(str)
control_data=control_data.set_index(["worker_identification","round_number"])
control_model=PanelOLS(control_data["effort"],control_data[["const","wage"]],entity_effects=False, drop_absorbed=True)
control_result=control_model.fit()
print("Basic OLS with no fixed effects, Effort After Data\n",control_result)

treatment_data["session_dummy"]=treatment_data["session"]
treatment_data=pd.get_dummies(treatment_data, columns=["session_dummy"])
treatment_data["worker_identification"]=treatment_data["session"].astype(str)+"_"+treatment_data["worker_id"].astype(str)
treatment_data=treatment_data.set_index(["worker_identification","round_number"])
treatment_model=PanelOLS(treatment_data["effort"],treatment_data[["const","wage"]],entity_effects=False, drop_absorbed=True)
treatment_result=treatment_model.fit()
print("Basic OLS with no fixed effects, Effort Before Data\n",treatment_result)

z_stat=(control_result.params["wage"]-treatment_result.params["wage"])/(math.sqrt(control_result.std_errors["wage"]**2+(treatment_result.std_errors["wage"])**2))
p_value=1-norm.cdf(z_stat)

# Basic OLS with individual fixed effects
control_data["session_dummy"]=control_data["session"]
control_data=pd.get_dummies(control_data, columns=["session_dummy"])
control_data["worker_identification"]=control_data["session"].astype(str)+"_"+control_data["worker_id"].astype(str)
control_model=PanelOLS(control_data["effort"],control_data[["const","wage"]],entity_effects=True, drop_absorbed=True)
control_result=control_model.fit()
print("Basic OLS with individual fixed effects, Effort After Data\n",control_result)

treatment_data["session_dummy"]=treatment_data["session"]
treatment_data=pd.get_dummies(treatment_data, columns=["session_dummy"])
treatment_data["worker_identification"]=treatment_data["session"].astype(str)+"_"+treatment_data["worker_id"].astype(str)
treatment_model=PanelOLS(treatment_data["effort"],treatment_data[["const","wage"]],entity_effects=True, drop_absorbed=True)
treatment_result=treatment_model.fit()
print("Basic OLS with individual fixed effects, Effort Before Data\n",treatment_result)

z_stat=(control_result.params["wage"]-treatment_result.params["wage"])/(math.sqrt(control_result.std_errors["wage"]**2+(treatment_result.std_errors["wage"])**2))
p_value=1-norm.cdf(z_stat)
print("Z-stats Basic OLS with individual fixed effects\n","z=",z_stat,", p=", p_value)

# Basic OLS with individual and time fixed effects
control_model=PanelOLS(control_data["effort"],control_data[["const","wage"]],entity_effects=True, time_effects=True, drop_absorbed=True)
control_result=control_model.fit()
print("Basic OLS with individual and period fixed effects, Effort After Data\n",control_result)

treatment_model=PanelOLS(treatment_data["effort"],treatment_data[["const","wage"]],entity_effects=True, time_effects=True, drop_absorbed=True)
treatment_result=treatment_model.fit()
print("Basic OLS with individual and period fixed effects, Effort Before Data\n",treatment_result)


z_stat=(control_result.params["wage"]-treatment_result.params["wage"])/(math.sqrt(control_result.std_errors["wage"]**2+(treatment_result.std_errors["wage"])**2))
p_value=1-norm.cdf(z_stat)
print("Z-stats Basic OLS with individual fixed effects\n", "z=",z_stat,", p=", p_value)

# One large Regression  
all_data["const"]=1
all_data["worker_identification"]=all_data["session"].astype(str)+"_"+all_data["worker_id"].astype(str)+all_data["treatment"].astype(str)
all_data=all_data.set_index(["worker_identification","round_number"])
all_data["EB_x_wage"]=all_data["treatment"]*all_data["wage"]
full_model=PanelOLS(all_data["effort"],all_data[["const","wage","EB_x_wage","treatment"]],entity_effects=False, time_effects=True, drop_absorbed=True)
full_result=full_model.fit()
print("Big OLS with individual and period fixed effects\n", full_result)

# One large Regression, with individual fixed effects
all_data["const"]=1
all_data["worker_identification"]=all_data["session"].astype(str)+"_"+all_data["worker_id"].astype(str)+all_data["treatment"].astype(str)
all_data["EB_x_wage"]=all_data["treatment"]*all_data["wage"]
full_model=PanelOLS(all_data["effort"],all_data[["const","wage","EB_x_wage","treatment"]],entity_effects=True, time_effects=True, drop_absorbed=True)
full_result=full_model.fit()
print(full_result)

control_data["total_surplus"]=control_data["worker_surplus"]+control_data["firm_surplus"]
treatment_data["total_surplus"]=treatment_data["worker_surplus"]+treatment_data["firm_surplus"]
control_data["worker_surplus_share"]=control_data["worker_surplus"]/control_data["total_surplus"]
treatment_data["worker_surplus_share"]=treatment_data["worker_surplus"]/treatment_data["total_surplus"]
control_averages=control_data.groupby("session").mean()
treatment_averages=treatment_data.groupby("session").mean()
effort_rank=ranksums(control_averages["effort"],treatment_averages["effort"], alternative="two-sided")
print("effort rank sum:", effort_rank)
wage_rank=ranksums(control_averages["wage"],treatment_averages["wage"], alternative="two-sided")
print("wage rank sum:",wage_rank)
worker_surplus_rank=ranksums(control_averages["worker_surplus"],treatment_averages["worker_surplus"], alternative="two-sided")
print("worker_surplus rank sum:",worker_surplus_rank)
firm_surplus_rank=ranksums(control_averages["firm_surplus"],treatment_averages["firm_surplus"], alternative="two-sided")
print("firm_surplus rank sum:",firm_surplus_rank)
total_surplus_rank=ranksums(control_averages["total_surplus"],treatment_averages["total_surplus"], alternative="two-sided")
print("total_surplus rank sum:",total_surplus_rank)
worker_surplus_share_rank=ranksums(control_averages["worker_surplus_share"],treatment_averages["worker_surplus_share"], alternative="two-sided")
print("worker_surplus_share rank sum:",worker_surplus_share_rank)








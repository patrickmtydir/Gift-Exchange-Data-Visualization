import seaborn as sb
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
import numpy as np
import math
from linearmodels.panel import PanelOLS
from scipy.stats import norm, ranksums
import builtins
import warnings
warnings.filterwarnings("ignore", message="The palette list has more values")
control_data=pd.DataFrame()
treatment_data=pd.DataFrame()
all_data=pd.DataFrame()
summary_stats=pd.DataFrame()
palette = sb.color_palette("colorblind")

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
        plt.savefig(file_path+"/Average Effort Per Wage "+f"{treatment} "+f"{session}"+".png", dpi=600)
        plt.clf()

        #Jitterplot
        ax=plt.gca()
        plt.title("Effort vs. Wage Jitterplot - "+session_title)
        jittered_x = data["wage"] + np.random.uniform(-0.3, 0.3, size=len(data))
        ax.scatter(jittered_x, data["effort"], color="black", alpha=0.6)
        sb.regplot(data=data, x="wage", y="effort", ax=ax, scatter=False, color='red', ci=None)
        plt.xlabel("Wage")
        plt.ylabel("Effort")
        plt.savefig(file_path+"/Effort Per Wage Jitterplot"+" "+f"{treatment} "+f"{session}"+".png", dpi=600)
        plt.clf()

        # Wages over time graph
        plt.title("Evolution of Wages Over Time - "+session_title)
        data["fixed_round"]=data["round_number"]-1
        data["round_number_plotting"]=data["fixed_round"]+(data["transaction_number"]/4)
        plt.xticks([1,2,3,4,5,6,7,8,9,10,11,12])
        sb.scatterplot(data=data, x=data["round_number_plotting"], y=data["wage"],color="black")
        plt.xlabel("Round Number")
        plt.ylabel("Wage")
        plt.savefig(file_path+"/Wage Offers Over Time"+" "+f"{treatment} "+f"{session}"+".png", dpi=600)
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
        wage_vs_effort_before_data["wage_offered"] = wage_vs_effort_before_data["wage_offered"] + np.random.uniform(-0.3, 0.3, size=len(wage_vs_effort_before_data))
        sb.scatterplot(data=wage_vs_effort_before_data, x=wage_vs_effort_before_data["effort_recieved"], y=wage_vs_effort_before_data["wage_offered"], ax=ax, color="black", alpha=0.4)
        sb.regplot(data=wage_vs_effort_before_data, x=wage_vs_effort_before_data["effort_recieved"], y=wage_vs_effort_before_data["wage_offered"], ax=ax, scatter=False, color='red', ci=None)
        #sb.stripplot(data=wage_vs_effort_before_data, x=wage_vs_effort_before_data["effort_recieved"], y=wage_vs_effort_before_data["wage_offered"], ax=ax, jitter=0.025 color="black", alpha=0.6)
        plt.xlabel("Effort Recieved in Round t")
        plt.ylabel("Wage offered in Round t+1")
        plt.savefig(file_path+"/Wage vs. Effort Recieved in Previous Round"+" "+f"{treatment} "+f"{session}"+".png", dpi=600)
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
        plt.savefig(file_path+"/Wage vs. Surplus Recieved in Previous Round"+" "+f"{treatment} "+f"{session}"+".png", dpi=600)
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

# Summary Table
mean_wage_groups_control=control_data.groupby(pd.cut(control_data['wage'], [29, 44, 59, 74, 89, 104, 126])).mean().round(2)
med_wage_groups_control=control_data.groupby(pd.cut(control_data['wage'], [29, 44, 59, 74, 89, 104, 126])).median().round(2)
count_wage_groups_control=control_data.groupby(pd.cut(control_data['wage'], [29, 44, 59, 74, 89, 104, 126])).count()
table_data_control={"Average Observed Effort Level":mean_wage_groups_control["effort"], "Median Observed Effort Level":med_wage_groups_control["effort"], "n":count_wage_groups_control["firm_id"]}
table_dataframe_control=pd.DataFrame(table_data_control)
custom_labels = ["30 to 44", "45 to 59", "60 to 74", "75 to 89", "90 to 104", "105 to 125"]
table_dataframe_control = table_dataframe_control.fillna("-")
table_dataframe_control.index = custom_labels
table_dataframe_control.index.name = "Wage Range"
table_dataframe_control["Average Observed Effort Level"]=table_dataframe_control["Average Observed Effort Level"].astype(str)
table_dataframe_control["Median Observed Effort Level"]=table_dataframe_control["Median Observed Effort Level"].astype(str)
str = builtins.str
with open("Summary Table Effort After.tex","w") as f:
    f.write(table_dataframe_control.to_latex(index=True, column_format="cccc", multirow=False))

mean_wage_groups_treatment=treatment_data.groupby(pd.cut(treatment_data['wage'], [29, 44, 59, 74, 89, 104, 126])).mean().round(2)
med_wage_groups_treatment=treatment_data.groupby(pd.cut(treatment_data['wage'], [29, 44, 59, 74, 89, 104, 126])).median().round(2)
count_wage_groups_treatment=treatment_data.groupby(pd.cut(treatment_data['wage'], [29, 44, 59, 74, 89, 104, 126])).count()
table_data_treatment={"Average Observed Effort Level":mean_wage_groups_treatment["effort"], "Median Observed Effort Level":med_wage_groups_treatment["effort"], "n":count_wage_groups_treatment["firm_id"]}
table_dataframe_treatment=pd.DataFrame(table_data_treatment)
custom_labels = ["30 to 44", "45 to 59", "60 to 74", "75 to 89", "90 to 104", "105 to 125"]
table_dataframe_treatment = table_dataframe_treatment.fillna("-")
table_dataframe_treatment.index = custom_labels
table_dataframe_treatment.index.name = "Wage Range"
table_dataframe_treatment["Average Observed Effort Level"]=table_dataframe_treatment["Average Observed Effort Level"].astype(str)
table_dataframe_treatment["Median Observed Effort Level"]=table_dataframe_treatment["Median Observed Effort Level"].astype(str)
str = builtins.str
with open("Summary Table Effort Before.tex","w") as f:
    f.write(table_dataframe_treatment.to_latex(index=True, column_format="cccc", multirow=False))

# Mean Observed Effort Graph
copy_data=all_data.copy(deep=False)
copy_data["treatment"]=copy_data["treatment"].replace({0:"Effort After", 1:"Effort Before"})
copy_data.rename(columns={'treatment': 'Treatment'}, inplace=True)
grouped_data=copy_data.groupby(["wage","session","Treatment"]).mean()
grouped_data_means=copy_data.groupby(["wage","Treatment"]).mean()
grouped_data_means=grouped_data_means.reset_index()

# Plot over average of sessions
ax=sb.lmplot(data=grouped_data_means, x="wage",y="effort", hue="Treatment", ci=0, palette=palette, fit_reg=True, legend=True)
ax.set(xlabel="Wage",ylabel="Average Effort", title="Aggregated Average Effort Per Wage", xticks=[30,50,70,90,110,130], yticks=[0,0.2,0.4,0.6,0.8,1])
ax.savefig("Aggregated Average Effort Per Wage", bbox_inches="tight", dpi=600)
plt.clf()

# Wages over time graph
data_round_fixed=copy_data.copy(deep=False)
data_round_fixed["round_number"]=data_round_fixed["round_number"]-1
data_round_fixed["round_number_plotting"]=data_round_fixed["round_number"]+(data_round_fixed["transaction_number"]/4)
ax=sb.lmplot(data=data_round_fixed, x="round_number_plotting", y="wage", x_jitter=0.1, y_jitter=0.1, hue="Treatment", palette=palette, scatter_kws={'alpha': 0.25}, ci=0, fit_reg=True, legend=False)
ax.set(xlabel="Round Number",ylabel="Wage", title="Evolution of Wages Over Time", xticks=[1,2,3,4,5,6,7,8,9,10,11,12], yticks=[30,50,70,90,110,130])
plt.legend(bbox_to_anchor=(1.0, 0.9), loc='upper right')
ax.figure.savefig("Aggregated Offers Over Time.png", bbox_inches="tight", dpi=600)
plt.clf()

# Wages over time graph 2
ax=sb.lmplot(data=data_round_fixed, x="round_number_plotting", y="wage", scatter=False, hue="Treatment", palette=palette, ci=90, fit_reg=True, legend=False)
ax.set(xlabel="Round Number",ylabel="Wage", title="Evolution of Wages Over Time", xticks=[1,2,3,4,5,6,7,8,9,10,11,12], yticks=[30,50,70,90,110,130])
plt.legend(bbox_to_anchor=(1.0, 0.9), loc='upper right')
ax.figure.savefig("Aggregated Offers Over Time Version 2.png", bbox_inches="tight", dpi=600)
plt.clf()

# Wages over time graph Separate
data_round_fixed_sep=control_data.copy(deep=False)
data_round_fixed_sep["round_number"]=data_round_fixed_sep["round_number"]-1
data_round_fixed_sep["round_number_plotting"]=data_round_fixed_sep["round_number"]+(data_round_fixed_sep["transaction_number"]/4)
ax=sb.lmplot(data=data_round_fixed_sep, x="round_number_plotting", y="wage", x_jitter=0.1, y_jitter=0.1, hue='treatment', palette= palette, scatter_kws={'alpha': 0.25}, ci=0, fit_reg=True, legend=False)
ax.set(xlabel="Round Number",ylabel="Wage", title="Evolution of Wages Over Time - Effort After", xticks=[1,2,3,4,5,6,7,8,9,10,11,12], yticks=[30,50,70,90,110,130])
ax.figure.savefig("Aggregated Offers Over Time Effort After.png", bbox_inches="tight", dpi=600)
plt.clf()

# Effort over time graph Separate
ax=sb.lmplot(data=data_round_fixed_sep, x="round_number_plotting", y="effort", x_jitter=0.1, y_jitter=0.05, hue='treatment', palette= palette, scatter_kws={'alpha': 0.25}, ci=0, fit_reg=True, legend=False)
ax.set(xlabel="Round Number",ylabel="Wage", title="Evolution of Effort Levels Over Time - Effort After", xticks=[1,2,3,4,5,6,7,8,9,10,11,12], yticks=[0,0.2,0.4,0.6,0.8,1])
ax.figure.savefig("Aggregated Effort Levels Over Time Effort After.png", bbox_inches="tight", dpi=600)
plt.clf()

# Wages over time graph Separate
data_round_fixed_sep=treatment_data.copy(deep=False)
data_round_fixed_sep["round_number"]=data_round_fixed_sep["round_number"]-1
data_round_fixed_sep["round_number_plotting"]=data_round_fixed_sep["round_number"]+(data_round_fixed_sep["transaction_number"]/4)
ax=sb.lmplot(data=data_round_fixed_sep, x="round_number_plotting", y="wage", x_jitter=0.1, y_jitter=0.1, hue='treatment', palette= [palette[1]], scatter_kws={'alpha': 0.25}, ci=0, fit_reg=True, legend=False)
ax.set(xlabel="Round Number",ylabel="Wage", title="Evolution of Wages Over Time - Effort Before", xticks=[1,2,3,4,5,6,7,8,9,10,11,12], yticks=[30,50,70,90,110,130])
ax.figure.savefig("Aggregated Offers Over Time Effort Before.png", bbox_inches="tight", dpi=600)
plt.clf()

# Effort over time graph Separate
ax=sb.lmplot(data=data_round_fixed_sep, x="round_number_plotting", y="effort", x_jitter=0.1, y_jitter=0.05, hue='treatment', palette= [palette[1]], scatter_kws={'alpha': 0.25}, ci=0, fit_reg=True, legend=False)
ax.set(xlabel="Round Number",ylabel="Wage", title="Evolution of Effort Levels Over Time - Effort Before", xticks=[1,2,3,4,5,6,7,8,9,10,11,12], yticks=[0,0.2,0.4,0.6,0.8,1])
ax.figure.savefig("Aggregated Effort Levels Over Time Effort Before.png", bbox_inches="tight", dpi=600)
plt.clf()

# Wage vs Effort Recieved in Previous Round - Effort After
ax=plt.gca()
plt.title("Wage vs. Effort Recieved in Previous Round - Effort After")
wage_vs_effort_before_list=[]
for row in range(len(control_data)):
    round_number_row=control_data.iloc[row]
    round_number=round_number_row["round_number"]
    session_number=round_number_row["session"]
    if round_number >1:
        firm_id=round_number_row["firm_id"]
        wage_offered=round_number_row["wage"]
        treatment=round_number_row["treatment"]
        previous_round=round_number-1
        effort_recieved_row=control_data.loc[(control_data["round_number"]==previous_round) & (control_data["firm_id"]==firm_id) & (control_data["session"]==session_number),"effort"]
        if len(effort_recieved_row)>0:
            effort_recieved=effort_recieved_row.item()
            wage_vs_effort_before_list.append({"round_number":round_number, "firm_id":firm_id, "effort_recieved":effort_recieved, "wage_offered":wage_offered, "session":session_number, "treatment":treatment})
wage_vs_effort_before_data=pd.DataFrame(wage_vs_effort_before_list)   
sb.regplot(data=wage_vs_effort_before_data, x=wage_vs_effort_before_data["effort_recieved"], y=wage_vs_effort_before_data["wage_offered"], ax=ax, scatter=False,color= palette[0], ci=None)
wage_vs_effort_before_data["wage_offered"] = wage_vs_effort_before_data["wage_offered"] + np.random.uniform(-2.5, 2.5, size=len(wage_vs_effort_before_data))
wage_vs_effort_before_data["effort_recieved"] = wage_vs_effort_before_data["effort_recieved"] + np.random.uniform(0, 0.05, size=len(wage_vs_effort_before_data))
sb.scatterplot(data=wage_vs_effort_before_data, x=wage_vs_effort_before_data["effort_recieved"], y=wage_vs_effort_before_data["wage_offered"], ax=ax, palette= palette, legend=False, hue=wage_vs_effort_before_data["treatment"], alpha=0.4)
#sb.stripplot(data=wage_vs_effort_before_data, x=wage_vs_effort_before_data["effort_recieved"], y=wage_vs_effort_before_data["wage_offered"], ax=ax, jitter=0.025 color="black", alpha=0.6)
plt.yticks([30,50,70,90,110,130])
plt.xlabel("Effort Recieved in Round t")
plt.ylabel("Wage offered in Round t+1")
plt.savefig("Wage vs. Effort Recieved in Previous Round - Effort After.png", bbox_inches="tight", dpi=600)
plt.clf()

# Wage vs Effort Recieved in Previous Round - Effort Before
ax=plt.gca()
plt.title("Wage vs. Effort Recieved in Previous Round - Effort Before")
wage_vs_effort_before_list=[]
for row in range(len(treatment_data)):
    round_number_row=treatment_data.iloc[row]
    round_number=round_number_row["round_number"]
    session_number=round_number_row["session"]
    if round_number >1:
        firm_id=round_number_row["firm_id"]
        wage_offered=round_number_row["wage"]
        treatment=round_number_row["treatment"]
        previous_round=round_number-1
        effort_recieved_row=treatment_data.loc[(treatment_data["round_number"]==previous_round) & (treatment_data["firm_id"]==firm_id) & (treatment_data["session"]==session_number),"effort"]
        if len(effort_recieved_row)>0:
            effort_recieved=effort_recieved_row.item()
            wage_vs_effort_before_list.append({"round_number":round_number, "firm_id":firm_id, "effort_recieved":effort_recieved, "wage_offered":wage_offered, "session":session_number, "treatment":treatment})
wage_vs_effort_before_data=pd.DataFrame(wage_vs_effort_before_list)   
sb.regplot(data=wage_vs_effort_before_data, x=wage_vs_effort_before_data["effort_recieved"], y=wage_vs_effort_before_data["wage_offered"], ax=ax, scatter=False, color= palette[1], ci=None)
wage_vs_effort_before_data["wage_offered"] = wage_vs_effort_before_data["wage_offered"] + np.random.uniform(-2.5, 2.5, size=len(wage_vs_effort_before_data))
wage_vs_effort_before_data["effort_recieved"] = wage_vs_effort_before_data["effort_recieved"] + np.random.uniform(0, 0.05, size=len(wage_vs_effort_before_data))
sb.scatterplot(data=wage_vs_effort_before_data, x=wage_vs_effort_before_data["effort_recieved"], y=wage_vs_effort_before_data["wage_offered"], ax=ax, palette= [palette[1]], legend=False, hue=wage_vs_effort_before_data["treatment"], alpha=0.4)
#sb.stripplot(data=wage_vs_effort_before_data, x=wage_vs_effort_before_data["effort_recieved"], y=wage_vs_effort_before_data["wage_offered"], ax=ax, jitter=0.025 color="black", alpha=0.6)
plt.yticks([30,50,70,90,110,130])
plt.xlabel("Effort Recieved in Round t")
plt.ylabel("Wage offered in Round t+1")
plt.savefig("Wage vs. Effort Recieved in Previous Round - Effort Before.png", bbox_inches="tight", dpi=600)
plt.clf()

#control_data = control_data.reset_index(drop=True)
#treatment_data = treatment_data.reset_index(drop=True)
# Wage vs Surplus Recieved in Previous Round - Effort After
ax=plt.gca()
plt.title("Wage vs. Surplus Recieved in Previous Round - Effort After")
wage_vs_surplus_before_list=[]
for row in range(len(control_data)):
    round_number_row=control_data.iloc[row]
    round_number=round_number_row["round_number"]
    session_number=round_number_row["session"]
    if round_number >1:
        firm_id=round_number_row["firm_id"]
        wage_offered=round_number_row["wage"]
        treatment=round_number_row["treatment"]
        previous_round=round_number-1
        surplus_recieved_row=control_data.loc[(control_data["round_number"]==previous_round) & (control_data["firm_id"]==firm_id) & (control_data["session"]==session_number),"firm_surplus"]
        if len(surplus_recieved_row)>0:
            surplus_recieved=surplus_recieved_row.item()
            wage_vs_surplus_before_list.append({"round_number":round_number, "firm_id":firm_id, "surplus_recieved":surplus_recieved, "wage_offered":wage_offered, "session":session_number, "treatment":treatment})
wage_vs_surplus_before_data=pd.DataFrame(wage_vs_surplus_before_list)
sb.regplot(data=wage_vs_surplus_before_data, x=wage_vs_surplus_before_data["surplus_recieved"], y=wage_vs_surplus_before_data["wage_offered"], ax=ax, scatter=False, color= palette[0], ci=None)
wage_vs_surplus_before_data["wage_offered"] = wage_vs_surplus_before_data["wage_offered"] + np.random.uniform(-2.5, 2.5, size=len(wage_vs_surplus_before_data))
sb.scatterplot(data=wage_vs_surplus_before_data, x=wage_vs_surplus_before_data["surplus_recieved"], y=wage_vs_surplus_before_data["wage_offered"], ax=ax, palette= palette, legend=False, hue=wage_vs_surplus_before_data["treatment"], alpha=0.4)
#sb.stripplot(data=wage_vs_surplus_before_data, x=wage_vs_surplus_before_data["surplus_recieved"], y=wage_vs_surplus_before_data["wage_offered"], jitter=True, color="black", alpha=0.6)
plt.xticks([0,10,20,30,40,50,60,70,80,90,100])
plt.yticks([30,50,70,90,110,130])
plt.xlabel("Surplus Recieved in Round t")
plt.ylabel("Wage offered in Round t+1")
plt.savefig("Wage vs. Surplus Recieved in Previous Round - Effort After.png", dpi=600, bbox_inches="tight")
plt.clf()

# Wage vs Surplus Recieved in Previous Round - Effort Before
ax=plt.gca()
plt.title("Wage vs. Surplus Recieved in Previous Round - Effort Before")
wage_vs_surplus_before_list=[]
for row in range(len(treatment_data)):
    round_number_row=treatment_data.iloc[row]
    round_number=round_number_row["round_number"]
    session_number=round_number_row["session"]
    if round_number >1:
        firm_id=round_number_row["firm_id"]
        wage_offered=round_number_row["wage"]
        treatment=round_number_row["treatment"]
        previous_round=round_number-1
        surplus_recieved_row=treatment_data.loc[(treatment_data["round_number"]==previous_round) & (treatment_data["firm_id"]==firm_id) & (treatment_data["session"]==session_number),"firm_surplus"]
        if len(surplus_recieved_row)>0:
            surplus_recieved=surplus_recieved_row.item()
            wage_vs_surplus_before_list.append({"round_number":round_number, "firm_id":firm_id, "surplus_recieved":surplus_recieved, "wage_offered":wage_offered, "session":session_number, "treatment":treatment})
wage_vs_surplus_before_data=pd.DataFrame(wage_vs_surplus_before_list)
sb.regplot(data=wage_vs_surplus_before_data, x=wage_vs_surplus_before_data["surplus_recieved"], y=wage_vs_surplus_before_data["wage_offered"], ax=ax, scatter=False, color= palette[1], ci=None)
wage_vs_surplus_before_data["wage_offered"] = wage_vs_surplus_before_data["wage_offered"] + np.random.uniform(-2.5, 2.5, size=len(wage_vs_surplus_before_data))
sb.scatterplot(data=wage_vs_surplus_before_data, x=wage_vs_surplus_before_data["surplus_recieved"], y=wage_vs_surplus_before_data["wage_offered"], ax=ax, palette= [palette[1]], legend=False, hue=wage_vs_surplus_before_data["treatment"], alpha=0.4)
#sb.stripplot(data=wage_vs_surplus_before_data, x=wage_vs_surplus_before_data["surplus_recieved"], y=wage_vs_surplus_before_data["wage_offered"], jitter=True, color="black", alpha=0.6)
plt.xticks([0,10,20,30,40,50,60,70,80,90,100])
plt.yticks([30,50,70,90,110,130])
plt.xlabel("Surplus Recieved in Round t")
plt.ylabel("Wage offered in Round t+1")
plt.savefig("Wage vs. Surplus Recieved in Previous Round - Effort Before.png", dpi=600, bbox_inches="tight")
plt.clf()

# Effort over time graph
ax=sb.lmplot(data=data_round_fixed, x="round_number_plotting", y="effort", x_jitter=0.1, y_jitter=0.1, hue="Treatment", palette=palette, scatter_kws={'alpha': 0.25}, ci=0, fit_reg=True, legend=False)
ax.set(xlabel="Round Number",ylabel="Effort", title="Evolution of Effort Over Time", xticks=[1,2,3,4,5,6,7,8,9,10,11,12], yticks=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0])
plt.legend(bbox_to_anchor=(1.0, 0.9), loc='upper right')
ax.figure.savefig("Aggregated Effort Levels Over Time.png", bbox_inches="tight", dpi=600)
plt.clf()

#Jitterplot
ax=sb.lmplot(data=data_round_fixed, x="wage", y="effort", x_jitter=0.05, y_jitter=0.05, hue="Treatment", scatter_kws={'alpha': 0.3}, ci=0, fit_reg=True, legend=False)
ax.set(xlabel="Wage",ylabel="Effort", title="Aggregated Effort vs. Wage", xticks=[30,50,70,90,110,130], yticks=[0,0.2,0.4,0.6,0.8,1])
plt.legend(bbox_to_anchor=(0.65, 1), loc='upper left')
plt.savefig("Aggregate Effort vs. Wage Jitter.png", bbox_inches="tight", dpi=600)
plt.clf()

# Empirical CDFs
ax=sb.ecdfplot(data=copy_data, x="effort", hue="Treatment", palette=palette, legend=True)
ax.set(xlabel="Effort", title="Empirical CDF of Effort Levels", xticks=[0,0.2,0.4,0.6,0.8,1.0], yticks=[0,0.2,0.4,0.6,0.8,1.0])
sb.move_legend(ax, "center right")
ax.figure.savefig("Empirical CDF of Effort", bbox_inches="tight", dpi=600)
plt.clf()

ax=sb.ecdfplot(data=copy_data, x="wage", hue="Treatment", palette=palette, legend=True)
ax.set(xlabel="Wage", title="Empirical CDF of Wages", xticks=[20,40,60,80,100,120], yticks=[0,0.2,0.4,0.6,0.8,1.0])
sb.move_legend(ax, "center right")
ax.figure.savefig("Empirical CDF of Wages", bbox_inches="tight", dpi=600)
plt.clf()

copy_data["total_surplus"]=copy_data["worker_surplus"]+copy_data["firm_surplus"]
copy_data["worker_surplus_share"]=copy_data["worker_surplus"]/copy_data["total_surplus"]

ax=sb.ecdfplot(data=copy_data, x="worker_surplus", hue="Treatment", palette=palette, legend=True)
ax.set(xlabel="Worker Surplus", title="Empirical CDF of Worker Surplus", xticks=[20,40,60,80,100], yticks=[0,0.2,0.4,0.6,0.8,1.0])
sb.move_legend(ax, "center right")
ax.figure.savefig("Empirical CDF of Worker Surplus", bbox_inches="tight", dpi=600)
plt.clf()

ax=sb.ecdfplot(data=copy_data, x="firm_surplus", hue="Treatment", palette=palette, legend=True)
ax.set(xlabel="Firm Surplus", title="Empirical CDF of Firm Surplus", xticks=[20,40,60,80,100], yticks=[0,0.2,0.4,0.6,0.8,1.0])
sb.move_legend(ax, "center right")
ax.figure.savefig("Empirical CDF of Firm Surplus", bbox_inches="tight", dpi=600)
plt.clf()

ax=sb.ecdfplot(data=copy_data, x="total_surplus", hue="Treatment", palette=palette, legend=True)
ax.set(xlabel="Total Surplus", title="Empirical CDF of Total Surplus", xticks=[20,40,60,80,100], yticks=[0,0.2,0.4,0.6,0.8,1.0])
sb.move_legend(ax, "center right")
ax.figure.savefig("Empirical CDF of Total Surplus", bbox_inches="tight", dpi=600)
plt.clf()

ax=sb.ecdfplot(data=copy_data, x="worker_surplus_share", hue="Treatment", palette=palette, legend=True)
ax.set(xlabel="Worker Surplus Share", title="Empirical CDF of Worker Surplus Shares", xticks=[0,0.2,0.4,0.6,0.8,1.0],yticks=[0,0.2,0.4,0.6,0.8,1.0])
sb.move_legend(ax, "center right", bbox_to_anchor=(1, 0.3))
ax.figure.savefig("Empirical CDF of Worker Surplus Shares", bbox_inches="tight", dpi=600)
plt.clf()

# Basic OLS with no fixed effects. Normalizing effort to be between 0 and 0.9 to avoid boundary issues and get true prosocial parameter
control_data["const"]=1
treatment_data["const"]=1
control_data["effort"]=control_data["effort"]-0.1
treatment_data["effort"]=treatment_data["effort"]-0.1

control_data["session_dummy"]=control_data["session"]
control_data=pd.get_dummies(control_data, columns=["session_dummy"])
control_data["worker_identification"]=control_data["session"].astype(str)+"_"+control_data["worker_id"].astype(str)
control_data["firm_identification"]=control_data["session"].astype(str)+"_"+control_data["firm_id"].astype(str)
control_data=control_data.set_index(["worker_identification","round_number"])
control_model=PanelOLS(control_data["effort"],control_data[["const","wage"]],entity_effects=False, drop_absorbed=True)
control_result=control_model.fit()
print("Basic OLS with no fixed effects, Effort After Data\n",control_result)

treatment_data["session_dummy"]=treatment_data["session"]
treatment_data=pd.get_dummies(treatment_data, columns=["session_dummy"])
treatment_data["worker_identification"]=treatment_data["session"].astype(str)+"_"+treatment_data["worker_id"].astype(str)
treatment_data["firm_identification"]=treatment_data["session"].astype(str)+"_"+treatment_data["firm_id"].astype(str)
treatment_data=treatment_data.set_index(["worker_identification","round_number"])
treatment_model=PanelOLS(treatment_data["effort"],treatment_data[["const","wage"]],entity_effects=False, drop_absorbed=True)
treatment_result=treatment_model.fit()
print("Basic OLS with no fixed effects, Effort Before Data\n",treatment_result)

z_stat=(control_result.params["wage"]-treatment_result.params["wage"])/(math.sqrt(control_result.std_errors["wage"]**2+(treatment_result.std_errors["wage"])**2))
p_value=1-norm.cdf(z_stat)
print("Z-stats Basic OLS with no fixed effects\n","z=",z_stat,", p=", p_value)
z_stat=(control_result.params["const"]-treatment_result.params["const"])/(math.sqrt(control_result.std_errors["const"]**2+(treatment_result.std_errors["const"])**2))
p_value=norm.cdf(z_stat)
print("Z-stats Basic OLS with no fixed effects CONST\n","z=",z_stat,", p=", p_value)

# Basic OLS with individual fixed effects
control_model=PanelOLS(control_data["effort"],control_data[["const","wage"]],entity_effects=True, drop_absorbed=True)
control_result=control_model.fit()
print("Basic OLS with individual fixed effects, Effort After Data\n",control_result)

treatment_model=PanelOLS(treatment_data["effort"],treatment_data[["const","wage"]],entity_effects=True, drop_absorbed=True)
treatment_result=treatment_model.fit()
print("Basic OLS with individual fixed effects, Effort Before Data\n",treatment_result)

z_stat=(control_result.params["wage"]-treatment_result.params["wage"])/(math.sqrt(control_result.std_errors["wage"]**2+(treatment_result.std_errors["wage"])**2))
p_value=1-norm.cdf(z_stat)
print("Z-stats Basic OLS with individual fixed effects\n","z=",z_stat,", p=", p_value)
z_stat=(control_result.params["const"]-treatment_result.params["const"])/(math.sqrt(control_result.std_errors["const"]**2+(treatment_result.std_errors["const"])**2))
p_value=norm.cdf(z_stat)
print("Z-stats Basic OLS with individual fixed effects CONST\n","z=",z_stat,", p=", p_value)

# Basic OLS with time fixed effects
control_model=PanelOLS(control_data["effort"],control_data[["const","wage"]],time_effects=True, drop_absorbed=True)
control_result=control_model.fit()
print("Basic OLS with period fixed effects, Effort After Data\n",control_result)

treatment_model=PanelOLS(treatment_data["effort"],treatment_data[["const","wage"]],time_effects=True, drop_absorbed=True)
treatment_result=treatment_model.fit()
print("Basic OLS with period fixed effects, Effort Before Data\n",treatment_result)

z_stat=(control_result.params["wage"]-treatment_result.params["wage"])/(math.sqrt(control_result.std_errors["wage"]**2+(treatment_result.std_errors["wage"])**2))
p_value=1-norm.cdf(z_stat)
print("Z-stats Basic OLS with time fixed effects\n","z=",z_stat,", p=", p_value)
z_stat=(control_result.params["const"]-treatment_result.params["const"])/(math.sqrt(control_result.std_errors["const"]**2+(treatment_result.std_errors["const"])**2))
p_value=norm.cdf(z_stat)
print("Z-stats Basic OLS with time fixed effects CONST\n","z=",z_stat,", p=", p_value)

# Basic OLS with individual and time fixed effects
control_model=PanelOLS(control_data["effort"],control_data[["const","wage"]],entity_effects=True, time_effects=True, drop_absorbed=True)
control_result=control_model.fit()
print("Basic OLS with individual and period fixed effects, Effort After Data\n",control_result)

treatment_model=PanelOLS(treatment_data["effort"],treatment_data[["const","wage"]],entity_effects=True, time_effects=True, drop_absorbed=True)
treatment_result=treatment_model.fit()
print("Basic OLS with individual and period fixed effects, Effort Before Data\n",treatment_result)


z_stat=(control_result.params["wage"]-treatment_result.params["wage"])/(math.sqrt(control_result.std_errors["wage"]**2+(treatment_result.std_errors["wage"])**2))
p_value=1-norm.cdf(z_stat)
print("Z-stats Basic OLS with individual and period fixed effects\n", "z=",z_stat,", p=", p_value)
z_stat=(control_result.params["const"]-treatment_result.params["const"])/(math.sqrt(control_result.std_errors["const"]**2+(treatment_result.std_errors["const"])**2))
p_value=norm.cdf(z_stat)
print("Z-stats Basic OLS with individual and period fixed effects CONST\n","z=",z_stat,", p=", p_value)

# Setting Up Simultaneous Regressions and also creating a csv file for R analysis
all_data["const"]=1
all_data["effort"]=all_data["effort"]-0.1
all_data["worker_identification"]=all_data["session"].astype(str)+"_"+all_data["worker_id"].astype(str)+all_data["treatment"].astype(str)
all_data["firm_identification"]=all_data["session"].astype(str)+"_"+all_data["firm_id"].astype(str)+all_data["treatment"].astype(str) 
all_data["total_surplus"]=all_data["worker_surplus"]+all_data["firm_surplus"]
all_data["worker_surplus_share"]=all_data["worker_surplus"]/all_data["total_surplus"]
all_data.to_csv("r_data.csv")
all_data=all_data.set_index(["worker_identification","round_number"])
all_data["EB_x_wage"]=all_data["treatment"]*all_data["wage"]


# Simultaneous Regression, no fixed effects
full_model=PanelOLS(all_data["effort"],all_data[["const","wage","EB_x_wage","treatment"]],entity_effects=False, time_effects=False, drop_absorbed=True)
full_result=full_model.fit()
print("Simultaneous OLS with no fixed effects\n", full_result)

# Simultaneous Regression, with period fixed effects
full_model=PanelOLS(all_data["effort"],all_data[["const","wage","EB_x_wage","treatment"]],entity_effects=False, time_effects=True, drop_absorbed=True)
full_result=full_model.fit()
print("Simultaneous OLS with period fixed effects\n", full_result)

# Simultaneous Regression, with period and individual fixed effects
full_model=PanelOLS(all_data["effort"],all_data[["const","wage","EB_x_wage","treatment"]],entity_effects=True, time_effects=True, drop_absorbed=True)
full_result=full_model.fit()
print("Simultaneous OLS with individual and period fixed effects\n", full_result)

# Simultaneous Regression, with period and session fixed effects
all_data=all_data.reset_index()
all_data["session_identification"]=all_data["session"].astype(str)+"_"+all_data["treatment"].astype(str)
all_data=all_data.set_index(["session_identification","round_number"])
full_model=PanelOLS(all_data["effort"],all_data[["const","wage","EB_x_wage","treatment"]],entity_effects=True, time_effects=True, drop_absorbed=True)
full_result=full_model.fit()
print("Simultaneous OLS with period and session fixed effects\n", full_result)
all_data=all_data.reset_index()
all_data=all_data.set_index(["worker_identification","round_number"])

# Simultaneous Regression, with individual fixed effects
full_model=PanelOLS(all_data["effort"],all_data[["const","wage","EB_x_wage","treatment"]],entity_effects=True, time_effects=False, drop_absorbed=True)
full_result=full_model.fit()
print("Simultaneous OLS with individual fixed effects\n", full_result)

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

#Round 1 analysis
control_data=control_data.reset_index()
treatment_data=treatment_data.reset_index()
control_data_round1=control_data[control_data["round_number"]==1]
treatment_data_round1=treatment_data[treatment_data["round_number"]==1]
control_averages_round1=control_data_round1.groupby("session").mean()
treatment_averages_round1=treatment_data_round1.groupby("session").mean()
wage_rank_round1=ranksums(control_averages_round1["wage"],treatment_averages_round1["wage"], alternative="two-sided")
print("wage rank sum ROUND 1:",wage_rank_round1)

#Payment Calculations
'''
def round_negative(value):
    if value < 0:
        return round(value)
    else:
        return value
'''

all_data=all_data.reset_index()
payment_worker_surplus=all_data.groupby("worker_identification").sum()["worker_surplus"]
#print("Minimum total surplus for a worker:",payment_worker_surplus.min())
# No bankrupt workers
payment_worker_surplus=payment_worker_surplus/25+7
num_subjects=payment_worker_surplus.size
payment_firm_surplus=all_data.groupby("firm_identification").sum()["firm_surplus"]
payment_firm_surplus=payment_firm_surplus/25+7
num_subjects=num_subjects+payment_firm_surplus.size
sum_firms=payment_firm_surplus.sum()
sum_workers=payment_worker_surplus.sum()
average_payment=(sum_workers+sum_firms)/num_subjects
#print(num_subjects) #To double check number of subjects is correct. Should be 140
print(average_payment)

#Calculate the average of initial wage offers in period 1 across treatments. 








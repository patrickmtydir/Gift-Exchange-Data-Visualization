import seaborn as sb
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
import numpy as np
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

    # End of session loop
# End of treatment loop   
    
# Mean Observed Effort Graph
copy_data=all_data.copy(deep=False)
copy_data["treatment"]=copy_data["treatment"].replace({0:"Effort After", 1:"Effort Before"})
copy_data.rename(columns={'treatment': 'Treatment'}, inplace=True)
grouped_data=copy_data.groupby(["wage","session","Treatment"]).mean()
grouped_data_means=copy_data.groupby(["wage","Treatment"]).mean()
grouped_data_means=grouped_data_means.reset_index()

# Plot over average of sessions, Presentation Graphs
ax=sb.lmplot(data=grouped_data_means, x="wage",y="effort", hue="Treatment", ci=0, palette=palette, fit_reg=True, legend=False)
plt.legend(loc='upper left')
ax.set(xlabel="Wage",ylabel="Average Effort", title="Aggregated Average Effort Per Wage", xticks=[30,50,70,90,110,130], yticks=[0,0.2,0.4,0.6,0.8,1])
ax.savefig("Aggregate Graphs/Aggregated Average Effort Per Wage", bbox_inches="tight", dpi=600)
plt.clf()
fehr_df=pd.DataFrame({
    "Treatment":["Fehr et al. 1993","Fehr et al. 1993","Fehr et al. 1993","Fehr et al. 1993","Fehr et al. 1993","Fehr et al. 1993","Fehr et al. 1993","Fehr et al. 1993","Fehr et al. 1993","Fehr et al. 1993","Fehr et al. 1993","Fehr et al. 1993","Fehr et al. 1993","Fehr et al. 1993","Fehr et al. 1993","Fehr et al. 1993","Fehr et al. 1993"],
    "wage": [30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110],
    "effort": [0.1, 0.1, 0.21, 0.11, 0.195, 0.2, 0.26, 0.25, 0.38, 0.35, 0.43, 0.58, 0.56, 0.37, 0.57, 0.59,1.0]
    })

grouped_data_means=grouped_data_means.append(fehr_df)
ax=sb.lmplot(data=fehr_df, x="wage",y="effort", hue="Treatment", ci=0, palette=[palette[4]], fit_reg=True, legend=False)
plt.legend(loc='upper left')
ax.set(xlabel="Wage",ylabel="Average Effort", title="Aggregated Average Effort Per Wage", xticks=[30,50,70,90,110,130], yticks=[0,0.2,0.4,0.6,0.8,1])
ax.savefig("Aggregate Graphs/Aggregated Average Effort Per Wage Fehr et al", bbox_inches="tight", dpi=600)
plt.clf()

pres_palette = [palette[0], palette[4]]
grouped_data_filtered = grouped_data_means[grouped_data_means["Treatment"].isin(["Effort After", "Fehr et al. 1993"])]
ax=sb.lmplot(data=grouped_data_filtered, x="wage",y="effort", hue="Treatment", ci=0, palette=pres_palette, fit_reg=True, legend=False)
plt.legend(loc='upper left')
ax.set(xlabel="Wage",ylabel="Average Effort", title="Aggregated Average Effort Per Wage", xticks=[30,50,70,90,110,130], yticks=[0,0.2,0.4,0.6,0.8,1])
ax.savefig("Aggregate Graphs/Aggregated Average Effort Per Wage Fehr et al vs Effort After", bbox_inches="tight", dpi=600)
plt.clf()


# Wages over time graph
data_round_fixed=copy_data.copy(deep=False)
data_round_fixed["round_number"]=data_round_fixed["round_number"]-1
data_round_fixed["round_number_plotting"]=data_round_fixed["round_number"]+(data_round_fixed["transaction_number"]/4)
ax=sb.lmplot(data=data_round_fixed, x="round_number_plotting", y="wage", x_jitter=0.1, y_jitter=0.1, hue="Treatment", palette=palette, scatter_kws={'alpha': 0.25}, ci=0, fit_reg=True, legend=False)
ax.set(xlabel="Round Number",ylabel="Wage", title="Evolution of Wages Over Time", xticks=[1,2,3,4,5,6,7,8,9,10,11,12], yticks=[30,50,70,90,110,130])
plt.legend(bbox_to_anchor=(1.0, 0.9), loc='upper right')
ax.figure.savefig("Aggregate Graphs/Aggregated Offers Over Time.png", bbox_inches="tight", dpi=600)
plt.clf()

# Wages over time graph 2
ax=sb.lmplot(data=data_round_fixed, x="round_number_plotting", y="wage", scatter=False, hue="Treatment", palette=palette, ci=90, fit_reg=True, legend=False)
ax.set(xlabel="Round Number",ylabel="Wage", title="Evolution of Wages Over Time", xticks=[1,2,3,4,5,6,7,8,9,10,11,12], yticks=[30,50,70,90,110,130])
plt.legend(bbox_to_anchor=(1.0, 0.9), loc='upper right')
ax.figure.savefig("Aggregate Graphs/Aggregated Offers Over Time Version 2.png", bbox_inches="tight", dpi=600)
plt.clf()

# Wages over time graph Separate
data_round_fixed_sep=control_data.copy(deep=False)
data_round_fixed_sep["round_number"]=data_round_fixed_sep["round_number"]-1
data_round_fixed_sep["round_number_plotting"]=data_round_fixed_sep["round_number"]+(data_round_fixed_sep["transaction_number"]/4)
ax=sb.lmplot(data=data_round_fixed_sep, x="round_number_plotting", y="wage", x_jitter=0.1, y_jitter=0.1, hue='treatment', palette= palette, scatter_kws={'alpha': 0.25}, ci=0, fit_reg=True, legend=False)
ax.set(xlabel="Round Number",ylabel="Wage", title="Evolution of Wages Over Time - Effort After", xticks=[1,2,3,4,5,6,7,8,9,10,11,12], yticks=[30,50,70,90,110,130])
ax.figure.savefig("Aggregate Graphs/Aggregated Offers Over Time Effort After.png", bbox_inches="tight", dpi=600)
plt.clf()

# Effort over time graph Separate
ax=sb.lmplot(data=data_round_fixed_sep, x="round_number_plotting", y="effort", x_jitter=0.1, y_jitter=0.05, hue='treatment', palette= palette, scatter_kws={'alpha': 0.25}, ci=0, fit_reg=True, legend=False)
ax.set(xlabel="Round Number",ylabel="Effort", title="Evolution of Effort Levels Over Time - Effort After", xticks=[1,2,3,4,5,6,7,8,9,10,11,12], yticks=[0,0.2,0.4,0.6,0.8,1])
ax.figure.savefig("Aggregate Graphs/Aggregated Effort Levels Over Time Effort After.png", bbox_inches="tight", dpi=600)
plt.clf()

# Wages over time graph Separate
data_round_fixed_sep=treatment_data.copy(deep=False)
data_round_fixed_sep["round_number"]=data_round_fixed_sep["round_number"]-1
data_round_fixed_sep["round_number_plotting"]=data_round_fixed_sep["round_number"]+(data_round_fixed_sep["transaction_number"]/4)
ax=sb.lmplot(data=data_round_fixed_sep, x="round_number_plotting", y="wage", x_jitter=0.1, y_jitter=0.1, hue='treatment', palette= [palette[1]], scatter_kws={'alpha': 0.25}, ci=0, fit_reg=True, legend=False)
ax.set(xlabel="Round Number",ylabel="Wage", title="Evolution of Wages Over Time - Effort Before", xticks=[1,2,3,4,5,6,7,8,9,10,11,12], yticks=[30,50,70,90,110,130])
ax.figure.savefig("Aggregate Graphs/Aggregated Offers Over Time Effort Before.png", bbox_inches="tight", dpi=600)
plt.clf()

# Effort over time graph Separate
ax=sb.lmplot(data=data_round_fixed_sep, x="round_number_plotting", y="effort", x_jitter=0.1, y_jitter=0.05, hue='treatment', palette= [palette[1]], scatter_kws={'alpha': 0.25}, ci=0, fit_reg=True, legend=False)
ax.set(xlabel="Round Number",ylabel="Effort", title="Evolution of Effort Levels Over Time - Effort Before", xticks=[1,2,3,4,5,6,7,8,9,10,11,12], yticks=[0,0.2,0.4,0.6,0.8,1])
ax.figure.savefig("Aggregate Graphs/Aggregated Effort Levels Over Time Effort Before.png", bbox_inches="tight", dpi=600)
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
        worker_id=round_number_row["worker_id"]
        wage_offered=round_number_row["wage"]
        treatment=round_number_row["treatment"]
        previous_round=round_number-1
        effort_recieved_row=control_data.loc[(control_data["round_number"]==previous_round) & (control_data["firm_id"]==firm_id) & (control_data["session"]==session_number),"effort"]
        if len(effort_recieved_row)>0:
            effort_recieved=effort_recieved_row.item()
            wage_vs_effort_before_list.append({"round_number":round_number, "firm_id":firm_id, "effort_recieved":effort_recieved, "wage_offered":wage_offered, "session":session_number, "treatment":treatment, "worker_id":worker_id})
wage_vs_effort_before_data=pd.DataFrame(wage_vs_effort_before_list) 
wage_vs_effort_before_data_control=wage_vs_effort_before_data.copy(deep=False) 
sb.regplot(data=wage_vs_effort_before_data, x=wage_vs_effort_before_data["effort_recieved"], y=wage_vs_effort_before_data["wage_offered"], ax=ax, scatter=False,color= palette[0], ci=None)
wage_vs_effort_before_data["wage_offered"] = wage_vs_effort_before_data["wage_offered"] + np.random.uniform(-2.5, 2.5, size=len(wage_vs_effort_before_data))
wage_vs_effort_before_data["effort_recieved"] = wage_vs_effort_before_data["effort_recieved"] + np.random.uniform(0, 0.05, size=len(wage_vs_effort_before_data))
sb.scatterplot(data=wage_vs_effort_before_data, x=wage_vs_effort_before_data["effort_recieved"], y=wage_vs_effort_before_data["wage_offered"], ax=ax, palette= palette, legend=False, hue=wage_vs_effort_before_data["treatment"], alpha=0.4)
#sb.stripplot(data=wage_vs_effort_before_data, x=wage_vs_effort_before_data["effort_recieved"], y=wage_vs_effort_before_data["wage_offered"], ax=ax, jitter=0.025 color="black", alpha=0.6)
plt.yticks([30,50,70,90,110,130])
plt.xlabel("Effort Recieved in Round t")
plt.ylabel("Wage offered in Round t+1")
plt.savefig("Aggregate Graphs/Wage vs. Effort Recieved in Previous Round - Effort After.png", bbox_inches="tight", dpi=600)
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
        worker_id=round_number_row["worker_id"]
        wage_offered=round_number_row["wage"]
        treatment=round_number_row["treatment"]
        previous_round=round_number-1
        effort_recieved_row=treatment_data.loc[(treatment_data["round_number"]==previous_round) & (treatment_data["firm_id"]==firm_id) & (treatment_data["session"]==session_number),"effort"]
        if len(effort_recieved_row)>0:
            effort_recieved=effort_recieved_row.item()
            wage_vs_effort_before_list.append({"round_number":round_number, "firm_id":firm_id, "effort_recieved":effort_recieved, "wage_offered":wage_offered, "session":session_number, "treatment":treatment, "worker_id":worker_id})
wage_vs_effort_before_data=pd.DataFrame(wage_vs_effort_before_list)   
wage_vs_effort_before_data_treatment=wage_vs_effort_before_data.copy(deep=False) 
sb.regplot(data=wage_vs_effort_before_data, x=wage_vs_effort_before_data["effort_recieved"], y=wage_vs_effort_before_data["wage_offered"], ax=ax, scatter=False, color= palette[1], ci=None)
wage_vs_effort_before_data["wage_offered"] = wage_vs_effort_before_data["wage_offered"] + np.random.uniform(-2.5, 2.5, size=len(wage_vs_effort_before_data))
wage_vs_effort_before_data["effort_recieved"] = wage_vs_effort_before_data["effort_recieved"] + np.random.uniform(0, 0.05, size=len(wage_vs_effort_before_data))
sb.scatterplot(data=wage_vs_effort_before_data, x=wage_vs_effort_before_data["effort_recieved"], y=wage_vs_effort_before_data["wage_offered"], ax=ax, palette= [palette[1]], legend=False, hue=wage_vs_effort_before_data["treatment"], alpha=0.4)
#sb.stripplot(data=wage_vs_effort_before_data, x=wage_vs_effort_before_data["effort_recieved"], y=wage_vs_effort_before_data["wage_offered"], ax=ax, jitter=0.025 color="black", alpha=0.6)
plt.yticks([30,50,70,90,110,130])
plt.xlabel("Effort Recieved in Round t")
plt.ylabel("Wage offered in Round t+1")
plt.savefig("Aggregate Graphs/Wage vs. Effort Recieved in Previous Round - Effort Before.png", bbox_inches="tight", dpi=600)
plt.clf()

# Effort over time graph
ax=sb.lmplot(data=data_round_fixed, x="round_number_plotting", y="effort", x_jitter=0.1, y_jitter=0.1, hue="Treatment", palette=palette, scatter_kws={'alpha': 0.25}, ci=0, fit_reg=True, legend=False)
ax.set(xlabel="Round Number",ylabel="Effort", title="Evolution of Effort Over Time", xticks=[1,2,3,4,5,6,7,8,9,10,11,12], yticks=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0])
plt.legend(bbox_to_anchor=(1.0, 0.9), loc='upper right')
ax.figure.savefig("Aggregate Graphs/Aggregated Effort Levels Over Time.png", bbox_inches="tight", dpi=600)
plt.clf()

#Jitterplot
ax=sb.lmplot(data=data_round_fixed, x="wage", y="effort", x_jitter=0.05, y_jitter=0.05, hue="Treatment", scatter_kws={'alpha': 0.3}, ci=0, fit_reg=True, legend=False)
ax.set(xlabel="Wage",ylabel="Effort", title="Aggregated Effort vs. Wage", xticks=[30,50,70,90,110,130], yticks=[0,0.2,0.4,0.6,0.8,1])
plt.legend(bbox_to_anchor=(0.65, 1), loc='upper left')
plt.savefig("Aggregate Graphs/Aggregate Effort vs. Wage Jitter.png", bbox_inches="tight", dpi=600)
plt.clf()

# Empirical CDFs
ax=sb.ecdfplot(data=copy_data, x="effort", hue="Treatment", palette=palette, legend=True)
ax.set(xlabel="Effort", title="Empirical CDF of Effort Levels", xticks=[0,0.2,0.4,0.6,0.8,1.0], yticks=[0,0.2,0.4,0.6,0.8,1.0])
sb.move_legend(ax, "center right")
ax.figure.savefig("Aggregate Graphs/Empirical CDF of Effort.png", bbox_inches="tight", dpi=600)
plt.clf()

ax=sb.ecdfplot(data=copy_data, x="wage", hue="Treatment", palette=palette, legend=True)
ax.set(xlabel="Wage", title="Empirical CDF of Wages", xticks=[20,40,60,80,100,120], yticks=[0,0.2,0.4,0.6,0.8,1.0])
sb.move_legend(ax, "center right")
ax.figure.savefig("Aggregate Graphs/Empirical CDF of Wages.png", bbox_inches="tight", dpi=600)
plt.clf()

copy_data["total_surplus"]=copy_data["worker_surplus"]+copy_data["firm_surplus"]
copy_data["worker_surplus_share"]=copy_data["worker_surplus"]/copy_data["total_surplus"]

ax=sb.ecdfplot(data=copy_data, x="worker_surplus", hue="Treatment", palette=palette, legend=True)
ax.set(xlabel="Worker Surplus", title="Empirical CDF of Worker Surplus", xticks=[20,40,60,80,100], yticks=[0,0.2,0.4,0.6,0.8,1.0])
sb.move_legend(ax, "center right")
ax.figure.savefig("Aggregate Graphs/Empirical CDF of Worker Surplus.png", bbox_inches="tight", dpi=600)
plt.clf()

ax=sb.ecdfplot(data=copy_data, x="firm_surplus", hue="Treatment", palette=palette, legend=True)
ax.set(xlabel="Firm Surplus", title="Empirical CDF of Firm Surplus", xticks=[20,40,60,80,100], yticks=[0,0.2,0.4,0.6,0.8,1.0])
sb.move_legend(ax, "center right")
ax.figure.savefig("Aggregate Graphs/Empirical CDF of Firm Surplus.png", bbox_inches="tight", dpi=600)
plt.clf()

ax=sb.ecdfplot(data=copy_data, x="total_surplus", hue="Treatment", palette=palette, legend=True)
ax.set(xlabel="Total Surplus", title="Empirical CDF of Total Surplus.png", xticks=[20,40,60,80,100], yticks=[0,0.2,0.4,0.6,0.8,1.0])
sb.move_legend(ax, "center right")
ax.figure.savefig("Aggregate Graphs/Empirical CDF of Total Surplus.png", bbox_inches="tight", dpi=600)
plt.clf()

ax=sb.ecdfplot(data=copy_data, x="worker_surplus_share", hue="Treatment", palette=palette, legend=True)
ax.set(xlabel="Worker Surplus Share", title="Empirical CDF of Worker Surplus Shares", xticks=[0,0.2,0.4,0.6,0.8,1.0],yticks=[0,0.2,0.4,0.6,0.8,1.0])
sb.move_legend(ax, "center right", bbox_to_anchor=(1, 0.3))
ax.figure.savefig("Aggregate Graphs/Empirical CDF of Worker Surplus Shares.png", bbox_inches="tight", dpi=600)
plt.clf()


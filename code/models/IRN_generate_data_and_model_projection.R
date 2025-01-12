# setwd("E:/GPL_covid/")
suppressPackageStartupMessages(library(tidyverse))
suppressPackageStartupMessages(library(lfe))
source("code/models/predict_felm.R")
source("code/models/projection_helper_functions.R")
<<<<<<< HEAD
underreporting <- read_csv("data/interim/multi_country/under_reporting.csv",
                           col_types = cols(
                             country = col_character(),
                             total_cases = col_double(),
                             total_deaths = col_double(),
                             underreporting_estimate = col_double(),
                             lower = col_double(),
                             upper = col_double(),
                             underreporting_estimate_clean = col_character()
                           ))
=======
>>>>>>> 3f7be048afb0e50d926b6a53b6ea7eb551308b51

iran_data <- read_csv("models/reg_data/IRN_reg_data.csv",
                   col_types = cols(
                     .default = col_double(),
                     adm0_name = col_character(),
                     adm1_name = col_character(),
                     date = col_date(format = ""),
                     adm1_id = col_character(),
                     t = col_character()
                   )) %>% 
  arrange(adm1_name, date) %>%
  mutate(adm1_id = factor(adm1_id),
         day_of_week = factor(dow),
         tmp_id = factor(adm1_id))

iran_data <- iran_data %>% 
  mutate_at(vars(matches("testing_regime")),
            ~if_else(is.na(.x), 0, .x))
<<<<<<< HEAD
=======
if(!(exists("gamma") & class(gamma) != "function")){
    gamma = readr::read_csv("models/gamma_est.csv",
                            col_types = 
                              cols(
                                recovery_delay = col_double(),
                                gamma = col_double()
                              )) %>% 
      filter(adm0_name %in% c("CHN", "KOR"), recovery_delay == 0) %>% 
      pull(gamma) %>% 
      mean()
}
if(!exists("underreporting")){
    underreporting <- read_csv("data/interim/multi_country/under_reporting.csv",
                               col_types = cols(
                                 country = col_character(),
                                 total_cases = col_double(),
                                 total_deaths = col_double(),
                                 underreporting_estimate = col_double(),
                                 lower = col_double(),
                                 upper = col_double(),
                                 underreporting_estimate_clean = col_character()
                               ))
}
>>>>>>> 3f7be048afb0e50d926b6a53b6ea7eb551308b51

changed = TRUE
while(changed){
  new <- iran_data %>% 
    group_by(tmp_id) %>% 
    filter(!(is.na(cum_confirmed_cases) & date == min(date)))  
  if(nrow(new) == nrow(iran_data)){
    changed <- FALSE
  }
  iran_data <- new
}

iran_policy_variables_to_use <- 
  c(
    names(iran_data) %>% str_subset('p_1'),
    names(iran_data) %>% str_subset('p_2')
  )  

iran_other_control_variables <- 
  c(names(iran_data) %>% str_subset("testing_regime_"),
    'day_of_week')

formula <- as.formula(
  paste("D_l_cum_confirmed_cases ~ tmp_id +", 
        paste(iran_policy_variables_to_use, collapse = " + "), ' + ',
        paste(iran_other_control_variables, collapse = " + "),
        " - 1 | 0 | 0 | date "
  ))

suppressWarnings({
  iran_model <- felm(data = iran_data,
                     formula = formula,
                     cmethod = 'reghdfe'); #summary(iran_model)
})
# debug(compute_predicted_cum_cases)
main_projection <- compute_predicted_cum_cases(full_data = iran_data, model = iran_model,
                                               lhs = "D_l_cum_confirmed_cases",
                                               policy_variables_used = iran_policy_variables_to_use,
                                               other_control_variables = iran_other_control_variables,
                                               gamma = gamma,
                                               proportion_confirmed = underreporting %>% 
                                                 filter(country == "Iran") %>% 
                                                 pull(underreporting_estimate))

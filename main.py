from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData

from functions import *
from const import *



def main():
    # Inputs
    amount_input = int(amount_input)+1
    
    with open(f"{SCENARIO_PATH}//Projects Documantation//Scenario_Information {new_name}.txt", mode='a') as f:
        get_txt_documantation('first', new_name)
        
    for x in range(0, amount_input):
        get_txt_documantation('second', new_name, number_of_scenario=x)
        measurements = []
        for index, measurement in enumerate(get_random_file()):
            measurements.append(create_final_format(f"{TRAJ_PATH}//{measurement}", MEASUREMENTS[index]))
        gps, rdr, opt, imu = measurements
        measurement_dict = {'GPS': gps, 'RDR': rdr, 'OPT': opt, 'IMU': imu}
        for measurement in measurement_dict:
            tstart_ave, tstart_ae, tstart_fve, tstart_fv, tstart_turn, tstart_ave, \
            tend_ave, tend_ae, tend_fve, tend_fv, azimuth, error_max = get_parameter_list()
            
            # Make sure start is not larger than end
            while not ((tstart_fv<tend_fv) and (tstart_ae<tend_ae) and (tstart_ave<tend_ave) and (tstart_fve<tend_fve)):
                # Extract the random parameters
                tstart_ave, tstart_ae, tstart_fve, tstart_fv, tstart_turn, tstart_ave, \
                tend_ave, tend_ae, tend_fve, tend_fv, azimuth, error_max = get_parameter_list()
                # Extract the random errors
                error_choices = get_errors()
                # Apply the errors with the parameters for each measurement
                measurement_dict[measurement], \
                errors_representation = apply_errors(measurement_dict=measurement_dict,
                                                    measurement=measurement, error_list=error_choices,
                                                    tstart_ave=tstart_ave, tstart_ae=tstart_ae, tstart_fve=tstart_fve,
                                                    tstart_fv=tstart_fv, tstart_turn=tstart_turn,
                                                    tend_ave=tend_ave, tend_ae=tend_ae, tend_fve=tend_fve,
                                                    tend_fv=tend_fv, azimuth=azimuth, error_max=error_max, t0=t0)
                
                # Record all the data in a txt file
                get_txt_documantation('third', new_name, x, measurement=measurement,
                                      errors_representation=errors_representation)
                # Save the data with the errors 
                save_file_by_measurement(measurement_dict, x, new_name)
                f.close()

if __name__ == '__main__':
    main()
    


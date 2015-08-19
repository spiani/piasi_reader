class MPHR(object):

    @staticmethod
    def read_mphr(f):
        mphr = MPHR()

        product_name = f.readline()
        mphr.product_name = product_name.split('=')[1].strip()
        
        parent_product_name1 = f.readline()
        mphr.parent_product_name1 = parent_product_name1.split('=')[1].strip()

        parent_product_name2 = f.readline()
        mphr.parent_product_name2 = parent_product_name2.split('=')[1].strip()

        parent_product_name3 = f.readline()
        mphr.parent_product_name3 = parent_product_name3.split('=')[1].strip()

        parent_product_name4 = f.readline()
        mphr.parent_product_name4 = parent_product_name4.split('=')[1].strip()

        instrument_id = f.readline()
        mphr.instrument_id = instrument_id.split('=')[1].strip()

        instrument_model = f.readline()
        mphr.instrument_model = instrument_model.split('=')[1].strip()

        product_type = f.readline()
        mphr.product_type = product_type.split('=')[1].strip()
        
        processing_level = f.readline()
        mphr.processing_level = processing_level.split('=')[1].strip()
        
        spacecraft_id = f.readline()
        mphr.spacecraft_id = spacecraft_id.split('=')[1].strip()
        
        sensing_start = f.readline()
        mphr.sensing_start = sensing_start.split('=')[1].strip()
        
        sensing_end = f.readline()
        mphr.sensing_end = sensing_end.split('=')[1].strip()
        
        sensing_start_theoretical = f.readline()
        mphr.sensing_start_theoretical = sensing_start_theoretical.split('=')[1].strip()
        
        sensing_end_theoretical = f.readline()
        mphr.sensing_end_theoretical = sensing_end_theoretical.split('=')[1].strip()
        
        processing_centre = f.readline()
        mphr.processing_centre = processing_centre.split('=')[1].strip()
        
        processor_major_version = f.readline()
        processor_major_version_raw = processor_major_version.split('=')[1].strip()
        if processor_major_version_raw == 'xxxxx':
            processor_major_version_raw = None
        mphr.processor_major_version = int(processor_major_version_raw)
        
        processor_minor_version = f.readline()
        processor_minor_version_raw = processor_minor_version.split('=')[1].strip()
        if processor_minor_version_raw == 'xxxxx':
            processor_minor_version_raw = None
        mphr.processor_minor_version = int(processor_minor_version_raw)

        format_major_version = f.readline()
        format_major_version_raw = format_major_version.split('=')[1].strip()
        if format_major_version_raw == 'xxxxx':
            format_major_version_raw = None
        mphr.format_major_version = int(format_major_version_raw)
    
        format_minor_version = f.readline()
        format_minor_version_raw = format_minor_version.split('=')[1].strip()
        if format_minor_version_raw == 'xxxxx':
            format_minor_version_raw = None
        mphr.format_minor_version = int(format_minor_version_raw)
        
        processing_time_start = f.readline()
        mphr.processing_time_start = processing_time_start.split('=')[1].strip()
        
        processing_time_end = f.readline()
        mphr.processing_time_end = processing_time_end.split('=')[1].strip()
        
        processing_mode = f.readline()
        mphr.processing_mode = processing_mode.split('=')[1].strip()
        
        disposition_mode = f.readline()
        mphr.disposition_mode = disposition_mode.split('=')[1].strip()
        
        receiving_ground_station = f.readline()
        mphr.receiving_ground_station = receiving_ground_station.split('=')[1].strip()
        
        receive_time_start = f.readline()
        mphr.receive_time_start = receive_time_start.split('=')[1].strip()
        
        receive_time_end = f.readline()
        mphr.receive_time_end = receive_time_end.split('=')[1].strip()
        
        orbit_start = f.readline()
        mphr.orbit_start = int(orbit_start.split('=')[1].strip())
        
        orbit_end = f.readline()
        mphr.orbit_end = int(orbit_end.split('=')[1].strip())
        
        actual_product_size = f.readline()
        mphr.actual_product_size = int(actual_product_size.split('=')[1].strip())

        state_vector_time = f.readline()
        mphr.state_vector_time = state_vector_time.split('=')[1].strip()

        scale = 1e0
        semi_major_axis = f.readline()
        mphr.semi_major_axis = float(semi_major_axis.split('=')[1].strip())/scale

        scale = 1e6
        eccentricity = f.readline()
        mphr.eccentricity = float(eccentricity.split('=')[1].strip())/scale

        scale = 1e3
        inclination = f.readline()
        mphr.inclination = float(inclination.split('=')[1].strip())/scale

        scale = 1e3
        perigee_argument = f.readline()
        mphr.perigee_argument = float(perigee_argument.split('=')[1].strip())/scale

        scale = 1e3
        right_ascension = f.readline()
        mphr.right_ascension = float(right_ascension.split('=')[1].strip())/scale

        scale = 1e3
        mean_anomaly = f.readline()
        mphr.mean_anomaly = float(mean_anomaly.split('=')[1].strip())/scale

        scale = 1e3
        x_position = f.readline()
        mphr.x_position = float(x_position.split('=')[1].strip())/scale
        
        scale = 1e3
        y_position = f.readline()
        mphr.y_position = float(y_position.split('=')[1].strip())/scale
        
        scale = 1e3
        z_position = f.readline()
        mphr.z_position = float(z_position.split('=')[1].strip())/scale
        
        scale = 1e3
        x_velocity = f.readline()
        mphr.x_velocity = float(x_velocity.split('=')[1].strip())/scale
        
        scale = 1e3
        y_velocity = f.readline()
        mphr.y_velocity = float(y_velocity.split('=')[1].strip())/scale
        
        scale = 1e3
        z_velocity = f.readline()
        mphr.z_velocity = float(z_velocity.split('=')[1].strip())/scale
        
        scale = 1e0
        earth_sun_distance_ratio = f.readline()
        mphr.earth_sun_distance_ratio = float(earth_sun_distance_ratio.split('=')[1].strip())/scale
        
        scale = 1e0
        location_tolerance_radial = f.readline()
        mphr.location_tolerance_radial = float(location_tolerance_radial.split('=')[1].strip())/scale
        
        scale = 1e0
        location_tolerance_crosstrack = f.readline()
        mphr.location_tolerance_crosstrack = float(location_tolerance_crosstrack.split('=')[1].strip())/scale
        
        scale = 1e0
        location_tolerance_alongtrack = f.readline()
        mphr.location_tolerance_alongtrack = float(location_tolerance_alongtrack.split('=')[1].strip())/scale
        
        scale = 1e3
        yaw_error = f.readline()
        mphr.yaw_error = float(yaw_error.split('=')[1].strip())/scale
        
        scale = 1e3
        roll_error = f.readline()
        mphr.roll_error = float(roll_error.split('=')[1].strip())/scale
        
        scale = 1e3
        pitch_error = f.readline()
        mphr.pitch_error = float(pitch_error.split('=')[1].strip())/scale
        
        scale = 1e3
        subsat_latitude_start = f.readline()
        subsat_latitude_start_raw = subsat_latitude_start.split('=')[1].strip()
        if 'x' in subsat_latitude_start_raw:
            mphr.subsat_latitude_start = None
        else:
            mphr.subsat_latitude_start = float(subsat_latitude_start_raw)/scale
        
        scale = 1e3
        subsat_longitude_start = f.readline()
        subsat_longitude_start_raw = subsat_longitude_start.split('=')[1].strip()
        if 'x' in subsat_longitude_start_raw:
            mphr.subsat_longitude_start = None
        else:
            mphr.subsat_longitude_start = float(subsat_longitude_start_raw)/scale
        
        scale = 1e3
        subsat_latitude_end = f.readline()
        subsat_latitude_end_raw = subsat_latitude_end.split('=')[1].strip()
        if 'x' in subsat_latitude_end_raw:
            mphr.subsat_latitude_end = None
        else:
            mphr.subsat_latitude_end = float(subsat_latitude_end_raw)/scale
        
        scale = 1e3
        subsat_longitude_end = f.readline()
        subsat_longitude_end_raw = subsat_longitude_end.split('=')[1].strip()
        if 'x' in subsat_longitude_end_raw:
            mphr.subsat_longitude_end = None
        else:
            mphr.subsat_longitude_end = float(subsat_longitude_end_raw)/scale
        
        leap_second = f.readline()
        mphr.leap_second = int(leap_second.split('=')[1].strip())
        
        leap_second_utc = f.readline()
        mphr.leap_second_utc = leap_second_utc.split('=')[1].strip()
        
        total_records = f.readline()
        mphr.total_records = int(total_records.split('=')[1].strip())
        
        total_mphr = f.readline()
        mphr.total_mphr = int(total_mphr.split('=')[1].strip())
        
        total_sphr = f.readline()
        mphr.total_sphr = int(total_sphr.split('=')[1].strip())
        
        total_ipr = f.readline()
        mphr.total_ipr = int(total_ipr.split('=')[1].strip())
        
        total_geadr = f.readline()
        mphr.total_geadr = int(total_geadr.split('=')[1].strip())
        
        total_giadr = f.readline()
        mphr.total_giadr = int(total_giadr.split('=')[1].strip())
        
        total_veadr = f.readline()
        mphr.total_veadr = int(total_veadr.split('=')[1].strip())
        
        total_viadr = f.readline()
        mphr.total_viadr = int(total_viadr.split('=')[1].strip())
        
        total_mdr = f.readline()
        mphr.total_mdr = int(total_mdr.split('=')[1].strip())
        
        count_degraded_inst_mdr = f.readline()
        mphr.count_degraded_inst_mdr = int(count_degraded_inst_mdr.split('=')[1].strip())
        
        count_degraded_proc_mdr = f.readline()
        mphr.count_degraded_proc_mdr = int(count_degraded_proc_mdr.split('=')[1].strip())
        
        count_degraded_inst_mdr_blocks = f.readline()
        mphr.count_degraded_inst_mdr_blocks = int(count_degraded_inst_mdr_blocks.split('=')[1].strip())
        
        count_degraded_proc_mdr_blocks = f.readline()
        mphr.count_degraded_proc_mdr_blocks = int(count_degraded_proc_mdr_blocks.split('=')[1].strip())
        
        duration_of_product = f.readline()
        mphr.duration_of_product = int(duration_of_product.split('=')[1].strip())
        
        milliseconds_of_data_present = f.readline()
        milliseconds_of_data_present_raw = milliseconds_of_data_present.split('=')[1].strip()
        if 'x' in milliseconds_of_data_present_raw:
            mphr.milliseconds_of_data_present = None
        else:
            mphr.milliseconds_of_data_present = int(milliseconds_of_data_present_raw)
        
        milliseconds_of_data_missing = f.readline()
        milliseconds_of_data_missing_raw = milliseconds_of_data_missing.split('=')[1].strip()
        if 'x' in milliseconds_of_data_missing_raw:
            mphr.milliseconds_of_data_missing = None
        else:
            mphr.milliseconds_of_data_missing = int(milliseconds_of_data_missing_raw)
        
        subsetted_product = f.readline()
        subsetted_product_raw = subsetted_product.split('=')[1].strip()
        if subsetted_product_raw == 'T':
            mphr.subsetted_product = True
        elif subsetted_product_raw == 'F':
            mphr.subsetted_product = False
        else:
            raise ValueError('Invalid value for subsetted product: ' + str(subsetted_product_raw))

        return mphr



    def __str__(self):
        output  = 'Product name:                   ' + str(self.product_name) + '\n'
        output += 'Parent product name 1:          ' + str(self.parent_product_name1) + '\n'
        output += 'Parent product name 2:          ' + str(self.parent_product_name2) + '\n'
        output += 'Parent product name 3:          ' + str(self.parent_product_name3) + '\n'
        output += 'Parent product name 4:          ' + str(self.parent_product_name4) + '\n'
        output += 'Instrument id:                  ' + str(self.instrument_id) + '\n'
        output += 'Instrument model:               ' + str(self.instrument_model) + '\n'
        output += 'Product type:                   ' + str(self.product_type) + '\n'
        output += 'Processing level:               ' + str(self.processing_level) + '\n'
        output += 'Spacecraft id:                  ' + str(self.spacecraft_id) + '\n'
        output += 'Sensing start:                  ' + str(self.sensing_start) + '\n'
        output += 'Sensing end:                    ' + str(self.sensing_end) + '\n'
        output += 'Sensing start theoretical:      ' + str(self.sensing_start_theoretical) + '\n'
        output += 'Sensing end theoretical:        ' + str(self.sensing_end_theoretical) + '\n'
        output += 'Processing centre:              ' + str(self.processing_centre) + '\n'
        output += 'Processor major version:        ' + str(self.processor_major_version) + '\n'
        output += 'Processor minor version:        ' + str(self.processor_minor_version) + '\n'
        output += 'Format major version:           ' + str(self.format_major_version) + '\n'
        output += 'Format minor version:           ' + str(self.format_minor_version) + '\n'
        output += 'Processing time start:          ' + str(self.processing_time_start) + '\n'
        output += 'Processing time end:            ' + str(self.processing_time_end) + '\n'
        output += 'Processing mode:                ' + str(self.processing_mode) + '\n'
        output += 'Disposition mode:               ' + str(self.disposition_mode) + '\n'
        output += 'Receiving ground station:       ' + str(self.receiving_ground_station) + '\n'
        output += 'Receive time start:             ' + str(self.receive_time_start) + '\n'
        output += 'Receive time end:               ' + str(self.receive_time_end) + '\n'
        output += 'Orbit start:                    ' + str(self.orbit_start) + '\n'
        output += 'Orbit end:                      ' + str(self.orbit_end) + '\n'
        output += 'Actual product size:            ' + str(self.actual_product_size) + '\n'
        output += 'State vector time:              ' + str(self.state_vector_time) + '\n'
        output += 'Semi major axis:                ' + str(self.semi_major_axis) + '\n'
        output += 'Eccentricity:                   ' + str(self.eccentricity) + '\n'
        output += 'Inclination:                    ' + str(self.inclination) + '\n'
        output += 'Perigee argument:               ' + str(self.perigee_argument) + '\n'
        output += 'Right ascension:                ' + str(self.right_ascension) + '\n'
        output += 'Mean anomaly:                   ' + str(self.mean_anomaly) + '\n'
        output += 'X position:                     ' + str(self.x_position) + '\n'
        output += 'Y position:                     ' + str(self.y_position) + '\n'
        output += 'Z position:                     ' + str(self.z_position) + '\n'
        output += 'X velocity:                     ' + str(self.x_velocity) + '\n'
        output += 'Y velocity:                     ' + str(self.y_velocity) + '\n'
        output += 'Z velocity:                     ' + str(self.z_velocity) + '\n'
        output += 'Earth sun distance ratio:       ' + str(self.earth_sun_distance_ratio) + '\n'
        output += 'Location tolerance radial:      ' + str(self.location_tolerance_radial) + '\n'
        output += 'Location tolerance crosstrack:  ' + str(self.location_tolerance_crosstrack) + '\n'
        output += 'Location tolerance alongtrack:  ' + str(self.location_tolerance_alongtrack) + '\n'
        output += 'Yaw error:                      ' + str(self.yaw_error) + '\n'
        output += 'Roll error:                     ' + str(self.roll_error) + '\n'
        output += 'Pitch error:                    ' + str(self.pitch_error) + '\n'
        output += 'Subsat latitude start:          ' + str(self.subsat_latitude_start) + '\n'
        output += 'Subsat longitude start:         ' + str(self.subsat_longitude_start) + '\n'
        output += 'Subsat latitude end:            ' + str(self.subsat_latitude_end) + '\n'
        output += 'Subsat longitude end:           ' + str(self.subsat_longitude_end) + '\n'
        output += 'Leap second:                    ' + str(self.leap_second) + '\n'
        output += 'Leap second utc:                ' + str(self.leap_second_utc) + '\n'
        output += 'Total records:                  ' + str(self.total_records) + '\n'
        output += 'Total mphr:                     ' + str(self.total_mphr) + '\n'
        output += 'Total sphr:                     ' + str(self.total_sphr) + '\n'
        output += 'Total ipr:                      ' + str(self.total_ipr) + '\n'
        output += 'Total geadr:                    ' + str(self.total_geadr) + '\n'
        output += 'Total giadr:                    ' + str(self.total_giadr) + '\n'
        output += 'Total veadr:                    ' + str(self.total_veadr) + '\n'
        output += 'Total viadr:                    ' + str(self.total_viadr) + '\n'
        output += 'Total mdr:                      ' + str(self.total_mdr) + '\n'
        output += 'Count degraded inst mdr:        ' + str(self.count_degraded_inst_mdr) + '\n'
        output += 'Count degraded proc mdr:        ' + str(self.count_degraded_proc_mdr) + '\n'
        output += 'Count degraded inst mdr blocks: ' + str(self.count_degraded_inst_mdr_blocks) + '\n'
        output += 'Count degraded proc mdr blocks: ' + str(self.count_degraded_proc_mdr_blocks) + '\n'
        output += 'Duration of product:            ' + str(self.duration_of_product) + '\n'
        output += 'Milliseconds of data present:   ' + str(self.milliseconds_of_data_present) + '\n'
        output += 'Milliseconds of data missing:   ' + str(self.milliseconds_of_data_missing) + '\n'
        output += 'Subsetted product:              ' + str(self.subsetted_product)
        return output

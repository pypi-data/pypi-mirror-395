def load_motor_and_stage_parameters():
    import lightcon.common
    from lightcon.datasets import load_json_data

    lightcon.common.motor_parameters = lightcon.datasets.load_json_data('motor_parameters.json')['Values']
    lightcon.common.stage_parameters = lightcon.datasets.load_json_data('stage_parameters.json')['Values']

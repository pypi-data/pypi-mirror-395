#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD. See https://nomad-lab.eu for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from nomad.config.models.plugins import AppEntryPoint
from nomad.config.models.ui import (
    App,
    Column,
    Menu,
    MenuSizeEnum,
    MenuItemTerms,
    MenuItemPeriodicTable,
    MenuItemHistogram,
    SearchQuantities,
)


schema = "pynxtools.nomad.schema.Root"

map_concept_to_full_quantities = {
    "Start Time": f"data.datetime#{schema}#datetime",
    "Entry Type": "entry_type",
    "Definition": f"data.ENTRY.definition__field#{schema}#str",
    "Periodic Table": "results.material.elements",
    # Scan Environment
    "Scan Mode": f"data.ENTRY.scan_mode__field#{schema}#str",
    "Head Temperature (Scan Environment)": f"data.ENTRY.INSTRUMENT.SCAN_ENVIRONMENT.head_temperature__field#{schema}#float",
    "Cryo Bottom Temperature (Scan Environment)": f"data.ENTRY.INSTRUMENT.SCAN_ENVIRONMENT.cryo_bottom_temperature__field#{schema}#float",
    "Cryo Shield Temperature (Scan Environment)": f"data.ENTRY.INSTRUMENT.SCAN_ENVIRONMENT.cryo_shield_temperature__field#{schema}#float",
    # Scan Environment->Topographic scan
    "offset x": f"data.ENTRY.INSTRUMENT.SCAN_ENVIRONMENT.SPM_SCAN_CONTROL.scan_region.scan_offset_value_x__field#{schema}#float",
    "offset y": f"data.ENTRY.INSTRUMENT.SCAN_ENVIRONMENT.SPM_SCAN_CONTROL.scan_region.scan_offset_value_y__field#{schema}#float",
    "scan points x": f"data.ENTRY.INSTRUMENT.SCAN_ENVIRONMENT.SPM_SCAN_CONTROL.meshSCAN.scan_points_x__field#{schema}#float",
    "scan points y": f"data.ENTRY.INSTRUMENT.SCAN_ENVIRONMENT.SPM_SCAN_CONTROL.meshSCAN.scan_points_y__field#{schema}#float",
    "step size x": f"data.ENTRY.INSTRUMENT.SCAN_ENVIRONMENT.SPM_SCAN_CONTROL.meshSCAN.step_size_x__field#{schema}#float",
    "step size y": f"data.ENTRY.INSTRUMENT.SCAN_ENVIRONMENT.SPM_SCAN_CONTROL.meshSCAN.step_size_y__field#{schema}#float",
    "scan range x": f"data.ENTRY.INSTRUMENT.SCAN_ENVIRONMENT.SPM_SCAN_CONTROL.scan_region.scan_range_x__field#{schema}#float",
    "scan range y": f"data.ENTRY.INSTRUMENT.SCAN_ENVIRONMENT.SPM_SCAN_CONTROL.scan_region.scan_range_y__field#{schema}#float",
    "scan angle x": f"data.ENTRY.INSTRUMENT.SCAN_ENVIRONMENT.SPM_SCAN_CONTROL.scan_region.scan_angle_x__field#{schema}#float",
    "scan angle y": f"data.ENTRY.INSTRUMENT.SCAN_ENVIRONMENT.SPM_SCAN_CONTROL.scan_region.scan_angle_y__field#{schema}#float",
    "scan start x": f"data.ENTRY.INSTRUMENT.SCAN_ENVIRONMENT.SPM_SCAN_CONTROL.scan_region.scan_start_x__field#{schema}#float",
    "scan start y": f"data.ENTRY.INSTRUMENT.SCAN_ENVIRONMENT.SPM_SCAN_CONTROL.scan_region.scan_start_y__field#{schema}#float",
    "scan end x": f"data.ENTRY.INSTRUMENT.SCAN_ENVIRONMENT.SPM_SCAN_CONTROL.scan_region.scan_end_x__field#{schema}#float",
    "scan end y": f"data.ENTRY.INSTRUMENT.SCAN_ENVIRONMENT.SPM_SCAN_CONTROL.scan_region.scan_end_y__field#{schema}#float",
    # Scan Environment -> Bias Scan
    "Bias Start (Bias Spectroscopy)": f"data.ENTRY.INSTRUMENT.bias_spectroscopy_environment.SPM_BIAS_SPECTROSCOPY.BIAS_SWEEP.scan_region.scan_start_bias__field#{schema}#float",
    "Bias End (Bias Spectroscopy)": f"data.ENTRY.INSTRUMENT.bias_spectroscopy_environment.SPM_BIAS_SPECTROSCOPY.BIAS_SWEEP.scan_region.scan_end_bias__field#{schema}#float",
    "Bias Offset (Bias Spectroscopy)": f"data.ENTRY.INSTRUMENT.bias_spectroscopy_environment.SPM_BIAS_SPECTROSCOPY.BIAS_SWEEP.scan_region.scan_offset_bias__field#{schema}#float",
    "Bias Range (Bias Spectroscopy)": f"data.ENTRY.INSTRUMENT.bias_spectroscopy_environment.SPM_BIAS_SPECTROSCOPY.BIAS_SWEEP.scan_region.scan_range_bias__field#{schema}#float",
    "Scan Points (Bias Spectroscopy)": f"data.ENTRY.INSTRUMENT.bias_spectroscopy_environment.SPM_BIAS_SPECTROSCOPY.BIAS_SWEEP.linear_sweep.scan_points_bias__field#{schema}#float",
    "Step Size (Bias Spectroscopy)": f"data.ENTRY.INSTRUMENT.bias_spectroscopy_environment.SPM_BIAS_SPECTROSCOPY.BIAS_SWEEP.linear_sweep.step_size_bias__field#{schema}#float",
    "z_offset (Bias Spectroscopy)": f"data.ENTRY.INSTRUMENT.bias_spectroscopy_environment.SPM_BIAS_SPECTROSCOPY.SPM_POSITIONER.z_controller.z_offset_value__field#{schema}#float",
    # Instrument -> Hardware
    "Name (Hardware)": f"data.ENTRY.INSTRUMENT.hardware.name__field#{schema}#str",
    "Model (Hardware)": f"data.ENTRY.INSTRUMENT.hardware.model__field#{schema}#str",
    # Instrument -> Software
    "Name (Software)": f"data.ENTRY.INSTRUMENT.software.name__field#{schema}#str",
    "Model (Software)": f"data.ENTRY.INSTRUMENT.software.model__field#{schema}#str",
    # Instrument -> current_sensor
    "Current (Current Sensor)": f"data.ENTRY.INSTRUMENT.current_sensorTAG.current__field#{schema}#float",
    "Current Offset (Current Sensor)": f"data.ENTRY.INSTRUMENT.current_sensorTAG.offset_value__field#{schema}#float",
    # Instrument -> voltage_sensor
    "Voltage (Voltage Sensor)": f"data.ENTRY.INSTRUMENT.voltage_sensorTAG.voltage__field#{schema}#float",
    "Voltage Offset (Voltage Sensor)": f"data.ENTRY.INSTRUMENT.voltage_sensorTAG.offset_value__field#{schema}#float",
    # Instrument -> Sample Bias Voltage
    "Bias voltage (Sample Bias Voltage)": f"data.ENTRY.INSTRUMENT.sample_bias_voltage.bias_voltage__field#{schema}#float",
    "Bias offset (Sample Bias Voltage)": f"data.ENTRY.INSTRUMENT.sample_bias_voltage.bias_offset_value__field#{schema}#float",
    # Instrument -> Piezo sensor
    "Piezo X (Piezo Sensor XYZ)": f"data.ENTRY.INSTRUMENT.piezo_sensor.x__field#{schema}#float",
    "Piezo Y (Piezo Sensor XYZ)": f"data.ENTRY.INSTRUMENT.piezo_sensor.y__field#{schema}#float",
    "Piezo Z (Piezo Sensor XYZ)": f"data.ENTRY.INSTRUMENT.piezo_sensor.z__field#{schema}#float",
    # Instrument -> Piezo Sensor -> SPM Positioner
    "controller label": f"data.ENTRY.INSTRUMENT.piezo_sensor.SPM_POSITIONER.controller_label__field#{schema}#str",
    "Z controller Set Point (Piezo Sensor)": f"data.ENTRY.INSTRUMENT.piezo_sensor.SPM_POSITIONER.z_controller.set_point__field#{schema}#float",
    "Z controller Z (Piezo Sensor)": f"data.ENTRY.INSTRUMENT.piezo_sensor.SPM_POSITIONER.z_controller.z__field#{schema}#float",
    # Instrument -> Lockin Amplifier
    "Reference Frequency (Lockin Amplifier)": f"data.ENTRY.INSTRUMENT.lockin_amplifier.reference_frequency__field#{schema}#float",
    "Reference Phase (Lockin Amplifier)": f"data.ENTRY.INSTRUMENT.lockin_amplifier.reference_phase__field#{schema}#float",
    "Reference Amplitude (Lockin Amplifier)": f"data.ENTRY.INSTRUMENT.lockin_amplifier.reference_amplitude__field#{schema}#float",
    "Demodulated signal (Lockin Amplifier)": f"data.ENTRY.INSTRUMENT.lockin_amplifier.demodulated_signal__field#{schema}#str",
    "Lockin Current Flip Sign (Lockin Amplifier)": f"data.ENTRY.INSTRUMENT.lockin_amplifier.flip_sign__field#{schema}#float",
    # AFM: Instrument -> Cantilever SPM
    "Reference Amplitude (Oscillator)": f"data.ENTRY.INSTRUMENT.SPM_CANTILEVER.cantilever_oscillator.reference_amplitude__field#{schema}#float",
    "Reference Frequency (Oscillator)": f"data.ENTRY.INSTRUMENT.SPM_CANTILEVER.cantilever_oscillator.reference_frequency__field#{schema}#float",
    "Reference Phase (Oscillator)": f"data.ENTRY.INSTRUMENT.SPM_CANTILEVER.cantilever_oscillator.reference_phase__field#{schema}#float",
}

spm_app = AppEntryPoint(
    name="SpmApp",
    description="A Generic NOMAD App for SPM Experimetal Technique.",
    app=App(
        # Label of the App
        label="SPM",
        # Path used in the URL, must be unique
        path="spm_app",
        # Used to categorize apps in the explore menu
        category="Experiment",
        # Brief description used in the app menu
        description="A simple search app customized for SPM experimental technique.",
        # Longer description that can also use markdown
        readme="This is a simple App to support basic search for NeXus based SPM Experiment Entries.",
        # If you want to use quantities from a custom schema, you need to load
        # the search quantities from it first here. Note that you can use a glob
        # syntax to load the entire package, or just a single schema from a
        # package.
        search_quantities=SearchQuantities(
            include=[f"*#{schema}"],
        ),
        # Controls which columns are shown in the results table
        columns=[
            Column(quantity="entry_id", selected=True),
            Column(quantity="entry_type", selected=True),
            Column(
                title="definition",
                quantity=f"data.ENTRY[*].definition__field#{schema}",
                selected=True,
            ),
            Column(
                title="Start Time",
                search_quantity=f"data.datetime#{schema}",
                selected=True,
            ),
            Column(
                title="Start Times by Entry",
                search_quantity=f"data.ENTRY[*].start_time__field#{schema}",
                selected=False,
            ),
            Column(
                title="title",
                quantity=f"data.ENTRY[*].title__field#{schema}",
                selected=True,
            ),
        ],
        # Dictionary of search filters that are always enabled for queries made
        # within this app. This is especially important to narrow down the
        # results to the wanted subset. Any available search filter can be
        # targeted here. This example makes sure that only entries that use
        # MySchema are included.
        filters_locked={"section_defs.definition_qualified_name": [schema]},
        # Controls the menu shown on the left
        menu=Menu(
            title="Filters",
            size=MenuSizeEnum.SM,
            show_header=True,
            items=[
                Menu(
                    title="Material",
                    size=MenuSizeEnum.XXL,
                    show_header=True,
                    items=[
                        MenuItemPeriodicTable(
                            quantity="results.material.elements",
                        ),
                        MenuItemTerms(
                            quantity="results.material.chemical_formula_hill",
                            width=6,
                            options=0,
                        ),
                        MenuItemTerms(
                            quantity="results.material.chemical_formula_iupac",
                            width=6,
                            options=0,
                        ),
                        MenuItemHistogram(
                            x="results.material.n_elements",
                        ),
                    ],
                ),
                Menu(
                    title="Scan Environment",
                ),
                Menu(
                    title="Temperature",
                    indentation=1,
                    show_header=True,
                    items=[
                        MenuItemHistogram(
                            title="Tip Temperature",
                            x=map_concept_to_full_quantities[
                                "Head Temperature (Scan Environment)"
                            ],
                        ),
                        MenuItemHistogram(
                            title="Cryo Bottom Temperature",
                            x=map_concept_to_full_quantities[
                                "Cryo Bottom Temperature (Scan Environment)"
                            ],
                        ),
                        MenuItemHistogram(
                            title="Cryo Shield Temperature",
                            x=map_concept_to_full_quantities[
                                "Cryo Shield Temperature (Scan Environment)"
                            ],
                        ),
                    ],
                ),
                Menu(
                    title="Scan Mode",
                    indentation=1,
                    show_header=True,
                    items=[
                        MenuItemTerms(
                            title="Scan Mode",
                            quantity=map_concept_to_full_quantities["Scan Mode"],
                        ),
                    ],
                ),
                Menu(
                    title="Topographic Scan",
                    indentation=1,
                    show_header=True,
                    # ),
                    # Menu(
                    #     title="Scan Region",
                    #     show_header=True,
                    #     indentation=2,
                    items=[
                        MenuItemHistogram(
                            title="Offset x",
                            x=map_concept_to_full_quantities["offset x"],
                        ),
                        MenuItemHistogram(
                            title="Offset y",
                            x=map_concept_to_full_quantities["offset y"],
                        ),
                        MenuItemHistogram(
                            title="Scan Range x",
                            x=map_concept_to_full_quantities["scan range x"],
                        ),
                        MenuItemHistogram(
                            title="Scan Range y",
                            x=map_concept_to_full_quantities["scan range y"],
                        ),
                        MenuItemHistogram(
                            title="Scan Angle x",
                            x=map_concept_to_full_quantities["scan angle x"],
                        ),
                        MenuItemHistogram(
                            title="Scan Angle y",
                            x=map_concept_to_full_quantities["scan angle y"],
                        ),
                        MenuItemHistogram(
                            title="Scan Points x",
                            x=map_concept_to_full_quantities["scan points x"],
                        ),
                        MenuItemHistogram(
                            title="Scan Points y",
                            x=map_concept_to_full_quantities["scan points y"],
                        ),
                        MenuItemHistogram(
                            title="Step Size x",
                            x=map_concept_to_full_quantities["step size x"],
                        ),
                        MenuItemHistogram(
                            title="Step Size y",
                            x=map_concept_to_full_quantities["step size y"],
                        ),
                        MenuItemHistogram(
                            title="Scan Start x",
                            x=map_concept_to_full_quantities["scan start x"],
                        ),
                        MenuItemHistogram(
                            title="Scan Start y",
                            x=map_concept_to_full_quantities["scan start y"],
                        ),
                        MenuItemHistogram(
                            title="Scan End x",
                            x=map_concept_to_full_quantities["scan end x"],
                        ),
                        MenuItemHistogram(
                            title="Scan End y",
                            x=map_concept_to_full_quantities["scan end y"],
                        ),
                    ],
                ),
                Menu(
                    title="Bias Scan (Bias Spectroscopy)",
                    indentation=1,
                    show_header=True,
                    items=[
                        MenuItemHistogram(
                            title="Bias Start",
                            x=map_concept_to_full_quantities[
                                "Bias Start (Bias Spectroscopy)"
                            ],
                        ),
                        MenuItemHistogram(
                            title="Bias End",
                            x=map_concept_to_full_quantities[
                                "Bias End (Bias Spectroscopy)"
                            ],
                        ),
                        MenuItemHistogram(
                            title="Bias Offset",
                            x=map_concept_to_full_quantities[
                                "Bias Offset (Bias Spectroscopy)"
                            ],
                        ),
                        MenuItemHistogram(
                            title="Bias Range",
                            x=map_concept_to_full_quantities[
                                "Bias Range (Bias Spectroscopy)"
                            ],
                        ),
                        MenuItemHistogram(
                            title="Scan Points",
                            x=map_concept_to_full_quantities[
                                "Scan Points (Bias Spectroscopy)"
                            ],
                        ),
                        MenuItemHistogram(
                            title="Step Size",
                            x=map_concept_to_full_quantities[
                                "Step Size (Bias Spectroscopy)"
                            ],
                        ),
                        MenuItemHistogram(
                            title="z_offset",
                            x=map_concept_to_full_quantities[
                                "z_offset (Bias Spectroscopy)"
                            ],
                        ),
                    ],
                ),
                Menu(
                    title="Instrument",
                ),
                Menu(
                    title="Cantilever SPM",
                    indentation=1,
                    show_header=True,
                    items=[
                        MenuItemHistogram(
                            title="Reference Amplitude (Oscillator)",
                            x=map_concept_to_full_quantities[
                                "Reference Amplitude (Oscillator)"
                            ],
                        ),
                        MenuItemHistogram(
                            title="Reference Frequency (Oscillator)",
                            x=map_concept_to_full_quantities[
                                "Reference Frequency (Oscillator)"
                            ],
                        ),
                        MenuItemHistogram(
                            title="Reference Phase (Oscillator)",
                            x=map_concept_to_full_quantities[
                                "Reference Phase (Oscillator)"
                            ],
                        ),
                    ],
                ),
                Menu(
                    title="Hardware",
                    indentation=1,
                    show_header=True,
                    items=[
                        MenuItemTerms(
                            title="Name (Hardware)",
                            quantity=map_concept_to_full_quantities["Name (Hardware)"],
                        ),
                        MenuItemTerms(
                            title="Model (Hardware)",
                            quantity=map_concept_to_full_quantities["Model (Hardware)"],
                        ),
                    ],
                ),
                Menu(
                    title="Software",
                    indentation=1,
                    show_header=True,
                    items=[
                        MenuItemTerms(
                            title="Name (Software)",
                            quantity=map_concept_to_full_quantities["Name (Software)"],
                        ),
                        MenuItemTerms(
                            title="Model (Software)",
                            quantity=map_concept_to_full_quantities["Model (Software)"],
                        ),
                    ],
                ),
                Menu(
                    title="Current Sensor",
                    indentation=1,
                    show_header=True,
                    items=[
                        MenuItemHistogram(
                            title="Current",
                            x=map_concept_to_full_quantities[
                                "Current (Current Sensor)"
                            ],
                        ),
                        MenuItemHistogram(
                            title="Current Offset",
                            x=map_concept_to_full_quantities[
                                "Current Offset (Current Sensor)"
                            ],
                        ),
                    ],
                ),
                Menu(
                    title="Lockin Amplifier",
                    indentation=1,
                    show_header=True,
                    items=[
                        MenuItemHistogram(
                            title="Reference Frequency",
                            x=map_concept_to_full_quantities[
                                "Reference Frequency (Lockin Amplifier)"
                            ],
                        ),
                        MenuItemHistogram(
                            title="Reference Phase",
                            x=map_concept_to_full_quantities[
                                "Reference Phase (Lockin Amplifier)"
                            ],
                        ),
                        MenuItemHistogram(
                            title="Reference Amplitude",
                            x=map_concept_to_full_quantities[
                                "Reference Amplitude (Lockin Amplifier)"
                            ],
                        ),
                        MenuItemTerms(
                            title="Demodulated signal",
                            quantity=map_concept_to_full_quantities[
                                "Demodulated signal (Lockin Amplifier)"
                            ],
                        ),
                        MenuItemHistogram(
                            title="Lockin Current Flip Sign",
                            x=map_concept_to_full_quantities[
                                "Lockin Current Flip Sign (Lockin Amplifier)"
                            ],
                        ),
                    ],
                ),
                Menu(
                    title="Voltage Sensor",
                    indentation=1,
                    show_header=True,
                    items=[
                        MenuItemHistogram(
                            title="Voltage",
                            x=map_concept_to_full_quantities[
                                "Voltage (Voltage Sensor)"
                            ],
                        ),
                        MenuItemHistogram(
                            title="Voltage Offset",
                            x=map_concept_to_full_quantities[
                                "Voltage Offset (Voltage Sensor)"
                            ],
                        ),
                    ],
                ),
                Menu(
                    title="Sample Bias Voltage",
                    indentation=1,
                    show_header=True,
                    items=[
                        MenuItemHistogram(
                            title="Bias Voltage",
                            x=map_concept_to_full_quantities[
                                "Bias voltage (Sample Bias Voltage)"
                            ],
                        ),
                        MenuItemHistogram(
                            title="Bias Offset",
                            x=map_concept_to_full_quantities[
                                "Bias offset (Sample Bias Voltage)"
                            ],
                        ),
                    ],
                ),
                Menu(
                    title="Piezo Sensor",
                    indentation=1,
                    show_header=True,
                    items=[
                        Menu(
                            title="SPM Positioner",
                            show_header=True,
                            items=[
                                MenuItemTerms(
                                    title="controller label",
                                    quantity=map_concept_to_full_quantities[
                                        "controller label"
                                    ],
                                ),
                                MenuItemHistogram(
                                    title="Set Point (Z controller)",
                                    x=map_concept_to_full_quantities[
                                        "Z controller Set Point (Piezo Sensor)"
                                    ],
                                ),
                                MenuItemHistogram(
                                    title="Z (Z controller)",
                                    x=map_concept_to_full_quantities[
                                        "Z controller Z (Piezo Sensor)"
                                    ],
                                ),
                            ],
                        ),
                        MenuItemHistogram(
                            title="x",
                            x=map_concept_to_full_quantities[
                                "Piezo X (Piezo Sensor XYZ)"
                            ],
                        ),
                        MenuItemHistogram(
                            title="y",
                            x=map_concept_to_full_quantities[
                                "Piezo Y (Piezo Sensor XYZ)"
                            ],
                        ),
                        MenuItemHistogram(
                            title="z",
                            x=map_concept_to_full_quantities[
                                "Piezo Z (Piezo Sensor XYZ)"
                            ],
                        ),
                    ],
                ),
                Menu(
                    title="Reproducibility & Resolution Indicators",
                ),
                Menu(
                    title="Temperature",
                    indentation=1,
                    show_header=True,
                    items=[
                        MenuItemHistogram(
                            title="Cantilever Tip Temperature",
                            x=map_concept_to_full_quantities[
                                "Head Temperature (Scan Environment)"
                            ],
                        ),
                        MenuItemHistogram(
                            title="Cryo Bottom Temperature",
                            x=map_concept_to_full_quantities[
                                "Cryo Bottom Temperature (Scan Environment)"
                            ],
                        ),
                        MenuItemHistogram(
                            title="Cryo Shield Temperature",
                            x=map_concept_to_full_quantities[
                                "Cryo Shield Temperature (Scan Environment)"
                            ],
                        ),
                    ],
                ),
                Menu(
                    title="Cantilever SPM",
                    indentation=1,
                    show_header=True,
                    items=[
                        MenuItemHistogram(
                            title="Cantilever Oscillator -> Reference Amplitude",
                            x=map_concept_to_full_quantities[
                                "Reference Amplitude (Oscillator)"
                            ],
                        ),
                        MenuItemHistogram(
                            title="Cantilever Oscillator -> Reference Frequency",
                            x=map_concept_to_full_quantities[
                                "Reference Frequency (Oscillator)"
                            ],
                        ),
                        MenuItemHistogram(
                            title="Cantilever Oscillator -> Reference Phase",
                            x=map_concept_to_full_quantities[
                                "Reference Phase (Oscillator)"
                            ],
                        ),
                    ],
                ),
                Menu(
                    title="Lockin Amplifier & Current Sensor",
                    indentation=1,
                    show_header=True,
                    items=[
                        MenuItemHistogram(
                            title="Reference Frequency",
                            x=map_concept_to_full_quantities[
                                "Reference Frequency (Lockin Amplifier)"
                            ],
                        ),
                        MenuItemHistogram(
                            title="Current",
                            x=map_concept_to_full_quantities[
                                "Current (Current Sensor)"
                            ],
                        ),
                        MenuItemHistogram(
                            title="Current Offset",
                            x=map_concept_to_full_quantities[
                                "Current Offset (Current Sensor)"
                            ],
                        ),
                    ],
                ),
                Menu(
                    title="Scan",
                    indentation=1,
                    show_header=True,
                    items=[
                        MenuItemHistogram(
                            title="Offset x",
                            x=map_concept_to_full_quantities["offset x"],
                        ),
                        MenuItemHistogram(
                            title="Offset y",
                            x=map_concept_to_full_quantities["offset y"],
                        ),
                        MenuItemHistogram(
                            title="Scan Range x",
                            x=map_concept_to_full_quantities["scan range x"],
                        ),
                        MenuItemHistogram(
                            title="Scan Range y",
                            x=map_concept_to_full_quantities["scan range y"],
                        ),
                        MenuItemHistogram(
                            title="Scan Points x",
                            x=map_concept_to_full_quantities["scan points x"],
                        ),
                        MenuItemHistogram(
                            title="Scan Points y",
                            x=map_concept_to_full_quantities["scan points y"],
                        ),
                        MenuItemHistogram(
                            title="Step Size x",
                            x=map_concept_to_full_quantities["step size x"],
                        ),
                        MenuItemHistogram(
                            title="Step Size y",
                            x=map_concept_to_full_quantities["step size y"],
                        ),
                        MenuItemHistogram(
                            title="Scan Start x",
                            x=map_concept_to_full_quantities["scan start x"],
                        ),
                        MenuItemHistogram(
                            title="Scan Start y",
                            x=map_concept_to_full_quantities["scan start y"],
                        ),
                        MenuItemHistogram(
                            title="Scan End x",
                            x=map_concept_to_full_quantities["scan end x"],
                        ),
                        MenuItemHistogram(
                            title="Scan End y",
                            x=map_concept_to_full_quantities["scan end y"],
                        ),
                    ],
                ),
                Menu(
                    title="Bias Spectroscopy",
                    indentation=1,
                    show_header=True,
                    items=[
                        MenuItemHistogram(
                            title="Bias Start (Bias Spectroscopy)",
                            x=map_concept_to_full_quantities[
                                "Bias Start (Bias Spectroscopy)"
                            ],
                        ),
                        MenuItemHistogram(
                            title="Bias End (Bias Spectroscopy)",
                            x=map_concept_to_full_quantities[
                                "Bias End (Bias Spectroscopy)"
                            ],
                        ),
                        MenuItemHistogram(
                            title="Bias Offset (Bias Spectroscopy)",
                            x=map_concept_to_full_quantities[
                                "Bias Offset (Bias Spectroscopy)"
                            ],
                        ),
                        MenuItemHistogram(
                            title="Bias Range (Bias Spectroscopy)",
                            x=map_concept_to_full_quantities[
                                "Bias Range (Bias Spectroscopy)"
                            ],
                        ),
                        MenuItemHistogram(
                            title="Scan Points (Bias Spectroscopy)",
                            x=map_concept_to_full_quantities[
                                "Scan Points (Bias Spectroscopy)"
                            ],
                        ),
                        MenuItemHistogram(
                            title="Step Size (Bias Spectroscopy)",
                            x=map_concept_to_full_quantities[
                                "Step Size (Bias Spectroscopy)"
                            ],
                        ),
                        MenuItemHistogram(
                            title="z_offset (Bias Spectroscopy)",
                            x=map_concept_to_full_quantities[
                                "z_offset (Bias Spectroscopy)"
                            ],
                        ),
                    ],
                ),
            ],
        ),
        dashboard={
            "widgets": [
                {
                    "type": "histogram",
                    "show_input": False,
                    "autorange": True,
                    "nbins": 30,
                    "scale": "linear",
                    "title": "Start Time",
                    "quantity": map_concept_to_full_quantities["Start Time"],
                    "layout": {
                        "xxl": {
                            "minH": 3,
                            "minW": 3,
                            "h": 5,
                            "w": 16,
                            "y": 11,
                            "x": 16,
                        },
                        "xl": {"minH": 3, "minW": 3, "h": 4, "w": 12, "y": 0, "x": 0},
                        "lg": {"minH": 3, "minW": 3, "h": 4, "w": 12, "y": 8, "x": 0},
                        "md": {"minH": 3, "minW": 3, "h": 4, "w": 12, "y": 0, "x": 0},
                        "sm": {"minH": 3, "minW": 3, "h": 4, "w": 12, "y": 0, "x": 0},
                    },
                },
                {
                    "type": "terms",
                    "show_input": False,
                    "scale": "linear",
                    "title": "Entry Type",
                    "quantity": map_concept_to_full_quantities["Entry Type"],
                    "layout": {
                        "xxl": {"minH": 3, "minW": 3, "h": 8, "w": 4, "y": 8, "x": 32},
                        "xl": {"minH": 3, "minW": 3, "h": 8, "w": 4, "y": 0, "x": 12},
                        "lg": {"minH": 3, "minW": 3, "h": 8, "w": 4, "y": 8, "x": 12},
                        "md": {"minH": 3, "minW": 3, "h": 8, "w": 4, "y": 0, "x": 12},
                        "sm": {"minH": 3, "minW": 3, "h": 8, "w": 4, "y": 46, "x": 0},
                    },
                },
                {
                    "type": "terms",
                    "show_input": False,
                    "scale": "linear",
                    "title": "Definition",
                    "quantity": "data.ENTRY.definition__field#pynxtools.nomad.schema.Root#str",
                    "layout": {
                        "xxl": {"minH": 3, "minW": 3, "h": 8, "w": 4, "y": 0, "x": 32},
                        "xl": {"minH": 3, "minW": 3, "h": 8, "w": 4, "y": 0, "x": 16},
                        "lg": {"minH": 3, "minW": 3, "h": 8, "w": 4, "y": 8, "x": 16},
                        "md": {"minH": 3, "minW": 3, "h": 8, "w": 4, "y": 38, "x": 0},
                        "sm": {"minH": 3, "minW": 3, "h": 8, "w": 4, "y": 38, "x": 0},
                    },
                },
                {
                    "type": "periodic_table",
                    "scale": "linear",
                    "title": "Periodic Table",
                    "quantity": map_concept_to_full_quantities["Periodic Table"],
                    "layout": {
                        "xxl": {
                            "minH": 3,
                            "minW": 3,
                            "h": 11,
                            "w": 16,
                            "y": 0,
                            "x": 16,
                        },
                        "xl": {"minH": 3, "minW": 3, "h": 4, "w": 12, "y": 4, "x": 0},
                        "lg": {"minH": 3, "minW": 3, "h": 8, "w": 18, "y": 0, "x": 0},
                        "md": {"minH": 3, "minW": 3, "h": 4, "w": 12, "y": 4, "x": 0},
                        "sm": {"minH": 3, "minW": 3, "h": 4, "w": 12, "y": 4, "x": 0},
                    },
                },
            ]
        },
    ),
)

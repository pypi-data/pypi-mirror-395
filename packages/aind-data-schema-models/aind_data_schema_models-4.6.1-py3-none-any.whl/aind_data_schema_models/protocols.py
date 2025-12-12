"""Protocols"""

import re
from typing import Union

from pydantic import ConfigDict, Field
from typing_extensions import Annotated

from aind_data_schema_models.pid_names import BaseName
from aind_data_schema_models.registries import Registry


class ProtocolModel(BaseName):
    """Base model for protocol"""

    model_config = ConfigDict(frozen=True)
    name: str
    version: int
    registry: Registry
    registry_identifier: str


class _Solenoid_Valve_Calibration_For_Behavior_Rigs_Utilizing_Water_Reward_V1(ProtocolModel):
    """Model Solenoid Valve Calibration for Behavior Rigs Utilizing Water Reward"""

    name: str = "Solenoid Valve Calibration for Behavior Rigs Utilizing Water Reward"
    version: int = 1
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.261gerq7dl47/v1"


class _Running_A_Dynamic_Foraging_Behavior_Task_In_Mice_V1(ProtocolModel):
    """Model Running a Dynamic Foraging Behavior Task in Mice"""

    name: str = "Running a Dynamic Foraging Behavior Task in Mice"
    version: int = 1
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.5jyl8p4m6g2w/v1"


class _Whole_Brain_Embedding_For_Smartspim_Easyindex_With_2_Agarose_V1(ProtocolModel):
    """Model Whole Brain Embedding for SmartSPIM - EasyIndex with 2% Agarose"""

    name: str = "Whole Brain Embedding for SmartSPIM - EasyIndex with 2% Agarose"
    version: int = 1
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.3byl4jpn8lo5/v1"


class _Stereotaxic_Injection_By_Nanoject_Protocol_V1(ProtocolModel):
    """Model Stereotaxic Injection by Nanoject Protocol"""

    name: str = "Stereotaxic Injection by Nanoject Protocol"
    version: int = 1
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.bd8qi9vw"


class _Stereotaxic_Injection_By_Nanoject_Protocol_V2(ProtocolModel):
    """Model Stereotaxic Injection by Nanoject Protocol"""

    name: str = "Stereotaxic Injection by Nanoject Protocol"
    version: int = 2
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.besfjebn"


class _Stereotaxic_Injection_By_Nanoject_Protocol_V3(ProtocolModel):
    """Model Stereotaxic Injection by Nanoject Protocol"""

    name: str = "Stereotaxic Injection by Nanoject Protocol"
    version: int = 3
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.bgpujvnw"


class _Stereotaxic_Injection_By_Nanoject_Protocol_V4(ProtocolModel):
    """Model Stereotaxic Injection by Nanoject Protocol"""

    name: str = "Stereotaxic Injection by Nanoject Protocol"
    version: int = 4
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.bp2l6nr7kgqe/v4"


class _Stereotaxic_Injection_By_Nanoject_Protocol_V5(ProtocolModel):
    """Model Stereotaxic Injection by Nanoject Protocol"""

    name: str = "Stereotaxic Injection by Nanoject Protocol"
    version: int = 5
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.bp2l6nr7kgqe/v5"


class _Stereotaxic_Injection_By_Nanoject_Protocol_V6(ProtocolModel):
    """Model Stereotaxic Injection by Nanoject Protocol"""

    name: str = "Stereotaxic Injection by Nanoject Protocol"
    version: int = 6
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.bp2l6nr7kgqe/v6"


class _Stereotaxic_Injection_By_Nanoject_Protocol_V7(ProtocolModel):
    """Model Stereotaxic Injection by Nanoject Protocol"""

    name: str = "Stereotaxic Injection by Nanoject Protocol"
    version: int = 7
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.bp2l6nr7kgqe/v7"


class _Stereotaxic_Injection_By_Iontophoresis_V1(ProtocolModel):
    """Model Stereotaxic Injection by Iontophoresis"""

    name: str = "Stereotaxic Injection by Iontophoresis"
    version: int = 1
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.bd8ti9wn"


class _Stereotaxic_Injection_By_Iontophoresis_V2(ProtocolModel):
    """Model Stereotaxic Injection by Iontophoresis"""

    name: str = "Stereotaxic Injection by Iontophoresis"
    version: int = 2
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.besgjebw"


class _Stereotaxic_Injection_By_Iontophoresis_V3(ProtocolModel):
    """Model Stereotaxic Injection by Iontophoresis"""

    name: str = "Stereotaxic Injection by Iontophoresis"
    version: int = 3
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.bgpvjvn6"


class _Stereotaxic_Injection_By_Iontophoresis_V4(ProtocolModel):
    """Model Stereotaxic Injection by Iontophoresis"""

    name: str = "Stereotaxic Injection by Iontophoresis"
    version: int = 4
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.14egn8ewzg5d/v4"


class _Stereotaxic_Injection_By_Iontophoresis_V5(ProtocolModel):
    """Model Stereotaxic Injection by Iontophoresis"""

    name: str = "Stereotaxic Injection by Iontophoresis"
    version: int = 5
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.14egn8ewzg5d/v5"


class _Stereotaxic_Injection_By_Iontophoresis_V6(ProtocolModel):
    """Model Stereotaxic Injection by Iontophoresis"""

    name: str = "Stereotaxic Injection by Iontophoresis"
    version: int = 6
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.14egn8ewzg5d/v6"


class _Stereotaxic_Injection_By_Iontophoresis_V7(ProtocolModel):
    """Model Stereotaxic Injection by Iontophoresis"""

    name: str = "Stereotaxic Injection by Iontophoresis"
    version: int = 7
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.14egn8ewzg5d/v7"


class _Mouse_Habituation_Head_Fixation_Into_Tube_V1(ProtocolModel):
    """Model Mouse Habituation - Head Fixation into Tube"""

    name: str = "Mouse Habituation - Head Fixation into Tube"
    version: int = 1
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.rm7vzxd74gx1/v1"


class _Mouse_Water_Restriction_V1(ProtocolModel):
    """Model Mouse Water Restriction"""

    name: str = "Mouse Water Restriction"
    version: int = 1
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.x54v9pn34g3e/v1"


class _Modified_Frame_Projected_Independent_Fiber_Photometry_Fip_System_Hardware_V1(ProtocolModel):
    """Model Modified Frame-projected  Independent Fiber  Photometry (FIP) System_Hardware"""

    name: str = "Modified Frame-projected  Independent Fiber  Photometry (FIP) System_Hardware"
    version: int = 1
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.261ge39edl47/v1"


class _Modified_Frame_Projected_Independent_Fiber_Photometry_Fip_System_Hardware_V2(ProtocolModel):
    """Model Modified Frame-projected  Independent Fiber  Photometry (FIP) System_Hardware"""

    name: str = "Modified Frame-projected  Independent Fiber  Photometry (FIP) System_Hardware"
    version: int = 2
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.261ge39edl47/v2"


class _Making_Agarose_For_Use_In_Acute_In_Vivo_Electrophysiology_Experiments__V1(ProtocolModel):
    """Model Making Agarose for use in acute in vivo Electrophysiology Experiments"""

    name: str = "Making Agarose for use in acute in vivo Electrophysiology Experiments "
    version: int = 1
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.5jyl8py89g2w/v1"


class _Plug_Removal_For_Acute_In_Vivo_Electrophysiology_Experiments_V1(ProtocolModel):
    """Model Plug Removal for acute in vivo Electrophysiology Experiments"""

    name: str = "Plug Removal for acute in vivo Electrophysiology Experiments"
    version: int = 1
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.eq2lywz8qvx9/v1"


class _Intraperitoneal_Injection_In_An_Adult_Mouse_V1(ProtocolModel):
    """Model Intraperitoneal Injection in an Adult Mouse"""

    name: str = "Intraperitoneal Injection in an Adult Mouse"
    version: int = 1
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.bfzgjp3w"


class _Intraperitoneal_Injection_In_An_Adult_Mouse_V2(ProtocolModel):
    """Model Intraperitoneal Injection in an Adult Mouse"""

    name: str = "Intraperitoneal Injection in an Adult Mouse"
    version: int = 2
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.5qpvo5w8dl4o/v2"


class _Multiplexed_Rna_Fish_On_Expanded_Mouse_Brain_Slices_V1(ProtocolModel):
    """Model Multiplexed RNA FISH on Expanded Mouse Brain Slices"""

    name: str = "Multiplexed RNA FISH on Expanded Mouse Brain Slices"
    version: int = 1
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.dm6gpzj28lzp/v1"


class _General_Setup_And_Takedown_Procedures_For_Rodent_Neurosurgery_V1(ProtocolModel):
    """Model General Setup and Takedown Procedures for Rodent Neurosurgery"""

    name: str = "General Setup and Takedown Procedures for Rodent Neurosurgery"
    version: int = 1
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.kqdg392o7g25/v1"


class _General_Setup_And_Takedown_Procedures_For_Rodent_Neurosurgery_V2(ProtocolModel):
    """Model General Setup and Takedown Procedures for Rodent Neurosurgery"""

    name: str = "General Setup and Takedown Procedures for Rodent Neurosurgery"
    version: int = 2
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.kqdg392o7g25/v2"


class _Dual_Hemisphere_Craniotomy_For_Electrophysiology_V1(ProtocolModel):
    """Model Dual Hemisphere Craniotomy for Electrophysiology"""

    name: str = "Dual Hemisphere Craniotomy for Electrophysiology"
    version: int = 1
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.rm7vzjoe2lx1/v1"


class _Aqueous_Sbip_Delipidation_For_Whole_Mouse_Brain_After_Morphofish_Perfusion__V1(ProtocolModel):
    """Model Aqueous (SBiP) Delipidation for Whole Mouse Brain After morphoFISH Perfusion"""

    name: str = "Aqueous (SBiP) Delipidation for Whole Mouse Brain After morphoFISH Perfusion "
    version: int = 1
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.rm7vzjz54lx1/v1"


class _Mouse_Habituation_Head_Fixation_On_Disk_V1(ProtocolModel):
    """Model Mouse Habituation - Head Fixation on Disk"""

    name: str = "Mouse Habituation - Head Fixation on Disk"
    version: int = 1
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.j8nlkojmxv5r/v1"


class _Mouse_Habituation_Head_Fixation_On_Disk_V2(ProtocolModel):
    """Model Mouse Habituation - Head Fixation on Disk"""

    name: str = "Mouse Habituation - Head Fixation on Disk"
    version: int = 2
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.j8nlkojmxv5r/v2"


class _Preparation_Of_Lipopolysaccharide_For_Intraperitoneal_Injection_V1(ProtocolModel):
    """Model Preparation of Lipopolysaccharide for Intraperitoneal Injection"""

    name: str = "Preparation of Lipopolysaccharide for Intraperitoneal Injection"
    version: int = 1
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.14egn9y1ml5d/v1"


class _Temporal_Assessment_Of_Immune_Response_V1(ProtocolModel):
    """Model Temporal Assessment of Immune Response"""

    name: str = "Temporal Assessment of Immune Response"
    version: int = 1
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.5jyl8dqx6g2w/v1"


class _Mouse_Vab_Catheter_Maintenance_V1(ProtocolModel):
    """Model Mouse VAB Catheter Maintenance"""

    name: str = "Mouse VAB Catheter Maintenance"
    version: int = 1
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.8epv52o5dv1b/v1"


class _Processing_Blood_Intended_For_Olink_Assay_V1(ProtocolModel):
    """Model Processing Blood Intended for Olink Assay"""

    name: str = "Processing Blood Intended for Olink Assay"
    version: int = 1
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.261ger81jl47/v1"


class _Barseq_2_5_V1(ProtocolModel):
    """Model BARseq 2.5"""

    name: str = "BARseq 2.5"
    version: int = 1
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.kqdg3ke9qv25/v1"


class _Aqueous_Sbip_Delipidation_Of_A_Whole_Mouse_Brain_V1(ProtocolModel):
    """Model Aqueous (SBiP) Delipidation of a Whole Mouse Brain"""

    name: str = "Aqueous (SBiP) Delipidation of a Whole Mouse Brain"
    version: int = 1
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.n2bvj81mwgk5/v1"


class _Aqueous_Sbip_Delipidation_Of_A_Whole_Mouse_Brain_V2(ProtocolModel):
    """Model Aqueous (SBiP) Delipidation of a Whole Mouse Brain"""

    name: str = "Aqueous (SBiP) Delipidation of a Whole Mouse Brain"
    version: int = 2
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.n2bvj81mwgk5/v2"


class _Tetrahydrofuran_And_Dichloromethane_Delipidation_Of_A_Whole_Mouse_Brain_V1(ProtocolModel):
    """Model Tetrahydrofuran and Dichloromethane Delipidation of a Whole Mouse Brain"""

    name: str = "Tetrahydrofuran and Dichloromethane Delipidation of a Whole Mouse Brain"
    version: int = 1
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.36wgqj1kxvk5/v1"


class _Tetrahydrofuran_And_Dichloromethane_Delipidation_Of_A_Whole_Mouse_Brain_V2(ProtocolModel):
    """Model Tetrahydrofuran and Dichloromethane Delipidation of a Whole Mouse Brain"""

    name: str = "Tetrahydrofuran and Dichloromethane Delipidation of a Whole Mouse Brain"
    version: int = 2
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.36wgqj1kxvk5/v2"


class _Whole_Mouse_Brain_Delipidation_Dichloromethane_V1(ProtocolModel):
    """Model Whole Mouse Brain Delipidation - Dichloromethane"""

    name: str = "Whole Mouse Brain Delipidation - Dichloromethane"
    version: int = 1
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.dm6gpj7n5gzp/v1"


class _Whole_Mouse_Brain_Delipidation_Immunolabeling_And_Expansion_Microscopy_V1(ProtocolModel):
    """Model Whole Mouse Brain Delipidation, Immunolabeling, and Expansion Microscopy"""

    name: str = "Whole Mouse Brain Delipidation, Immunolabeling, and Expansion Microscopy"
    version: int = 1
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.n92ldpwjxl5b/v1"


class _Immunolabeling_Of_A_Whole_Mouse_Brain_V1(ProtocolModel):
    """Model Immunolabeling of a Whole Mouse Brain"""

    name: str = "Immunolabeling of a Whole Mouse Brain"
    version: int = 1
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.ewov1okwylr2/v1"


class _Structural_Mri_Using_The_University_Of_Washington_14T_Vertical_Bore_Bruker_Mri_V1(ProtocolModel):
    """Model Structural MRI Using the University of Washington 14T Vertical Bore Bruker MRI"""

    name: str = "Structural MRI Using the University of Washington 14T Vertical Bore Bruker MRI"
    version: int = 1
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.3byl4j8p2lo5/v1"


class _Duragel_Application_For_Acute_Electrophysiology_Recordings_V1(ProtocolModel):
    """Model Duragel Application for Acute Electrophysiology Recordings"""

    name: str = "Duragel Application for Acute Electrophysiology Recordings"
    version: int = 1
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.14egn2dwqg5d/v1"


class _Smartspim_Setup_And_Alignment_V1(ProtocolModel):
    """Model SmartSPIM setup and alignment"""

    name: str = "SmartSPIM setup and alignment"
    version: int = 1
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.5jyl8jyb7g2w/v1"


class _Refractive_Index_Matching_Easyindex_V1(ProtocolModel):
    """Model Refractive Index Matching - EasyIndex"""

    name: str = "Refractive Index Matching - EasyIndex"
    version: int = 1
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.kxygx965kg8j/v1"


class _Preparing_A_3D_Printed_Implant_For_Acute_In_Vivo_Electrophysiology_V1(ProtocolModel):
    """Model Preparing a 3D Printed Implant for Acute In Vivo Electrophysiology"""

    name: str = "Preparing a 3D Printed Implant for Acute In Vivo Electrophysiology"
    version: int = 1
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.6qpvr4jmogmk/v1"


class _Imaging_Cleared_Mouse_Brains_On_Smartspim_V1(ProtocolModel):
    """Model Imaging cleared mouse brains on SmartSPIM"""

    name: str = "Imaging cleared mouse brains on SmartSPIM"
    version: int = 1
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.3byl4jo1rlo5/v1"


class _Refractive_Index_Matching_Ethyl_Cinnamate_V1(ProtocolModel):
    """Model Refractive Index Matching - Ethyl Cinnamate"""

    name: str = "Refractive Index Matching - Ethyl Cinnamate"
    version: int = 1
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.n2bvj8k4bgk5/v1"


class _Dapi_Staining_Mouse_Brain_Sections_V1(ProtocolModel):
    """Model DAPI Staining Mouse Brain Sections"""

    name: str = "DAPI Staining Mouse Brain Sections"
    version: int = 1
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.3byl4jm6rlo5/v1"


class _Modified_Frame_Projected_Independent_Fiber_Photometry_Fip_System_Triggering_System_V1(ProtocolModel):
    """Model Modified Frame-projected Independent Fiber Photometry (FIP) System_Triggering system"""

    name: str = "Modified Frame-projected Independent Fiber Photometry (FIP) System_Triggering system"
    version: int = 1
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.kxygx3e6wg8j/v1"


class _Multi_Site_Optic_Fiber_Implants_V1(ProtocolModel):
    """Model Multi-Site Optic Fiber Implants"""

    name: str = "Multi-Site Optic Fiber Implants"
    version: int = 1
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.6qpvr3dqovmk/v1"


class _Immunohistochemistry_Ihc_Staining_Mouse_Brain_Sections_V1(ProtocolModel):
    """Model Immunohistochemistry (IHC) Staining Mouse Brain Sections"""

    name: str = "Immunohistochemistry (IHC) Staining Mouse Brain Sections"
    version: int = 1
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.5qpvo3b7bv4o/v1"


class _Sectioning_Mouse_Brain_With_Sliding_Microtome_V1(ProtocolModel):
    """Model Sectioning Mouse Brain with Sliding Microtome"""

    name: str = "Sectioning Mouse Brain with Sliding Microtome"
    version: int = 1
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.5jyl8p97rg2w/v1"


class _Mounting_And_Coverslipping_Mouse_Brain_Sections_V1(ProtocolModel):
    """Model Mounting and Coverslipping Mouse Brain Sections"""

    name: str = "Mounting and Coverslipping Mouse Brain Sections"
    version: int = 1
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.n92ldmpy7l5b/v1"


class _Stereotactic_Injections_With_Headframe_Implant_V1(ProtocolModel):
    """Model Stereotactic Injections with Headframe Implant"""

    name: str = "Stereotactic Injections with Headframe Implant"
    version: int = 1
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.eq2lyj72elx9/v1"


class _Protocol_Collection_Perfusing_Sectioning_Ihc_Mounting_And_Coverslipping_Mouse_Brain_Specimens_V1(ProtocolModel):
    """Model Protocol Collection: Perfusing, Sectioning, IHC, Mounting and Coverslipping Mouse Brain Specimens"""

    name: str = "Protocol Collection: Perfusing, Sectioning, IHC, Mounting and Coverslipping Mouse Brain Specimens"
    version: int = 1
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.kxygx3yxkg8j/v1"


class _Mouse_Cardiac_Perfusion_Fixation_And_Brain_Collection_V1(ProtocolModel):
    """Model Mouse Cardiac Perfusion Fixation and Brain Collection"""

    name: str = "Mouse Cardiac Perfusion Fixation and Brain Collection"
    version: int = 1
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.bd8vi9w6"


class _Mouse_Cardiac_Perfusion_Fixation_And_Brain_Collection_V2(ProtocolModel):
    """Model Mouse Cardiac Perfusion Fixation and Brain Collection"""

    name: str = "Mouse Cardiac Perfusion Fixation and Brain Collection"
    version: int = 2
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.besijece"


class _Mouse_Cardiac_Perfusion_Fixation_And_Brain_Collection_V3(ProtocolModel):
    """Model Mouse Cardiac Perfusion Fixation and Brain Collection"""

    name: str = "Mouse Cardiac Perfusion Fixation and Brain Collection"
    version: int = 3
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.beudjes6"


class _Mouse_Cardiac_Perfusion_Fixation_And_Brain_Collection_V4(ProtocolModel):
    """Model Mouse Cardiac Perfusion Fixation and Brain Collection"""

    name: str = "Mouse Cardiac Perfusion Fixation and Brain Collection"
    version: int = 4
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.be2djga6"


class _Mouse_Cardiac_Perfusion_Fixation_And_Brain_Collection_V5(ProtocolModel):
    """Model Mouse Cardiac Perfusion Fixation and Brain Collection"""

    name: str = "Mouse Cardiac Perfusion Fixation and Brain Collection"
    version: int = 5
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.bg5vjy66"


class _Mouse_Cardiac_Perfusion_Fixation_And_Brain_Collection_V6(ProtocolModel):
    """Model Mouse Cardiac Perfusion Fixation and Brain Collection"""

    name: str = "Mouse Cardiac Perfusion Fixation and Brain Collection"
    version: int = 6
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.8epv51bejl1b/v6"


class _Mouse_Cardiac_Perfusion_Fixation_And_Brain_Collection_V7(ProtocolModel):
    """Model Mouse Cardiac Perfusion Fixation and Brain Collection"""

    name: str = "Mouse Cardiac Perfusion Fixation and Brain Collection"
    version: int = 7
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.8epv51bejl1b/v7"


class _Mouse_Cardiac_Perfusion_Fixation_And_Brain_Collection_V8(ProtocolModel):
    """Model Mouse Cardiac Perfusion Fixation and Brain Collection"""

    name: str = "Mouse Cardiac Perfusion Fixation and Brain Collection"
    version: int = 8
    registry: Registry = Registry.DOI
    registry_identifier: str = "10.17504/protocols.io.8epv51bejl1b/v8"


class Protocols:
    """Protocols"""

    SOLENOID_VALVE_CALIBRATION_FOR_BEHAVIOR_RIGS_UTILIZING_WATER_REWARD_V1 = (
        _Solenoid_Valve_Calibration_For_Behavior_Rigs_Utilizing_Water_Reward_V1()
    )

    RUNNING_A_DYNAMIC_FORAGING_BEHAVIOR_TASK_IN_MICE_V1 = _Running_A_Dynamic_Foraging_Behavior_Task_In_Mice_V1()

    WHOLE_BRAIN_EMBEDDING_FOR_SMARTSPIM___EASYINDEX_WITH_2__AGAROSE_V1 = (
        _Whole_Brain_Embedding_For_Smartspim_Easyindex_With_2_Agarose_V1()
    )

    STEREOTAXIC_INJECTION_BY_NANOJECT_PROTOCOL_V1 = _Stereotaxic_Injection_By_Nanoject_Protocol_V1()

    STEREOTAXIC_INJECTION_BY_NANOJECT_PROTOCOL_V2 = _Stereotaxic_Injection_By_Nanoject_Protocol_V2()

    STEREOTAXIC_INJECTION_BY_NANOJECT_PROTOCOL_V3 = _Stereotaxic_Injection_By_Nanoject_Protocol_V3()

    STEREOTAXIC_INJECTION_BY_NANOJECT_PROTOCOL_V4 = _Stereotaxic_Injection_By_Nanoject_Protocol_V4()

    STEREOTAXIC_INJECTION_BY_NANOJECT_PROTOCOL_V5 = _Stereotaxic_Injection_By_Nanoject_Protocol_V5()

    STEREOTAXIC_INJECTION_BY_NANOJECT_PROTOCOL_V6 = _Stereotaxic_Injection_By_Nanoject_Protocol_V6()

    STEREOTAXIC_INJECTION_BY_NANOJECT_PROTOCOL_V7 = _Stereotaxic_Injection_By_Nanoject_Protocol_V7()

    STEREOTAXIC_INJECTION_BY_IONTOPHORESIS_V1 = _Stereotaxic_Injection_By_Iontophoresis_V1()

    STEREOTAXIC_INJECTION_BY_IONTOPHORESIS_V2 = _Stereotaxic_Injection_By_Iontophoresis_V2()

    STEREOTAXIC_INJECTION_BY_IONTOPHORESIS_V3 = _Stereotaxic_Injection_By_Iontophoresis_V3()

    STEREOTAXIC_INJECTION_BY_IONTOPHORESIS_V4 = _Stereotaxic_Injection_By_Iontophoresis_V4()

    STEREOTAXIC_INJECTION_BY_IONTOPHORESIS_V5 = _Stereotaxic_Injection_By_Iontophoresis_V5()

    STEREOTAXIC_INJECTION_BY_IONTOPHORESIS_V6 = _Stereotaxic_Injection_By_Iontophoresis_V6()

    STEREOTAXIC_INJECTION_BY_IONTOPHORESIS_V7 = _Stereotaxic_Injection_By_Iontophoresis_V7()

    MOUSE_HABITUATION___HEAD_FIXATION_INTO_TUBE_V1 = _Mouse_Habituation_Head_Fixation_Into_Tube_V1()

    MOUSE_WATER_RESTRICTION_V1 = _Mouse_Water_Restriction_V1()

    MODIFIED_FRAME_PROJECTED__INDEPENDENT_FIBER__PHOTOMETRY__FIP__SYSTEM_HARDWARE_V1 = (
        _Modified_Frame_Projected_Independent_Fiber_Photometry_Fip_System_Hardware_V1()
    )

    MODIFIED_FRAME_PROJECTED__INDEPENDENT_FIBER__PHOTOMETRY__FIP__SYSTEM_HARDWARE_V2 = (
        _Modified_Frame_Projected_Independent_Fiber_Photometry_Fip_System_Hardware_V2()
    )

    MAKING_AGAROSE_FOR_USE_IN_ACUTE_IN_VIVO_ELECTROPHYSIOLOGY_EXPERIMENTS__V1 = (
        _Making_Agarose_For_Use_In_Acute_In_Vivo_Electrophysiology_Experiments__V1()
    )

    PLUG_REMOVAL_FOR_ACUTE_IN_VIVO_ELECTROPHYSIOLOGY_EXPERIMENTS_V1 = (
        _Plug_Removal_For_Acute_In_Vivo_Electrophysiology_Experiments_V1()
    )

    INTRAPERITONEAL_INJECTION_IN_AN_ADULT_MOUSE_V1 = _Intraperitoneal_Injection_In_An_Adult_Mouse_V1()

    INTRAPERITONEAL_INJECTION_IN_AN_ADULT_MOUSE_V2 = _Intraperitoneal_Injection_In_An_Adult_Mouse_V2()

    MULTIPLEXED_RNA_FISH_ON_EXPANDED_MOUSE_BRAIN_SLICES_V1 = _Multiplexed_Rna_Fish_On_Expanded_Mouse_Brain_Slices_V1()

    GENERAL_SETUP_AND_TAKEDOWN_PROCEDURES_FOR_RODENT_NEUROSURGERY_V1 = (
        _General_Setup_And_Takedown_Procedures_For_Rodent_Neurosurgery_V1()
    )

    GENERAL_SETUP_AND_TAKEDOWN_PROCEDURES_FOR_RODENT_NEUROSURGERY_V2 = (
        _General_Setup_And_Takedown_Procedures_For_Rodent_Neurosurgery_V2()
    )

    DUAL_HEMISPHERE_CRANIOTOMY_FOR_ELECTROPHYSIOLOGY_V1 = _Dual_Hemisphere_Craniotomy_For_Electrophysiology_V1()

    AQUEOUS__SBIP__DELIPIDATION_FOR_WHOLE_MOUSE_BRAIN_AFTER_MORPHOFISH_PERFUSION__V1 = (
        _Aqueous_Sbip_Delipidation_For_Whole_Mouse_Brain_After_Morphofish_Perfusion__V1()
    )

    MOUSE_HABITUATION___HEAD_FIXATION_ON_DISK_V1 = _Mouse_Habituation_Head_Fixation_On_Disk_V1()

    MOUSE_HABITUATION___HEAD_FIXATION_ON_DISK_V2 = _Mouse_Habituation_Head_Fixation_On_Disk_V2()

    PREPARATION_OF_LIPOPOLYSACCHARIDE_FOR_INTRAPERITONEAL_INJECTION_V1 = (
        _Preparation_Of_Lipopolysaccharide_For_Intraperitoneal_Injection_V1()
    )

    TEMPORAL_ASSESSMENT_OF_IMMUNE_RESPONSE_V1 = _Temporal_Assessment_Of_Immune_Response_V1()

    MOUSE_VAB_CATHETER_MAINTENANCE_V1 = _Mouse_Vab_Catheter_Maintenance_V1()

    PROCESSING_BLOOD_INTENDED_FOR_OLINK_ASSAY_V1 = _Processing_Blood_Intended_For_Olink_Assay_V1()

    BARSEQ_2_5_V1 = _Barseq_2_5_V1()

    AQUEOUS__SBIP__DELIPIDATION_OF_A_WHOLE_MOUSE_BRAIN_V1 = _Aqueous_Sbip_Delipidation_Of_A_Whole_Mouse_Brain_V1()

    AQUEOUS__SBIP__DELIPIDATION_OF_A_WHOLE_MOUSE_BRAIN_V2 = _Aqueous_Sbip_Delipidation_Of_A_Whole_Mouse_Brain_V2()

    TETRAHYDROFURAN_AND_DICHLOROMETHANE_DELIPIDATION_OF_A_WHOLE_MOUSE_BRAIN_V1 = (
        _Tetrahydrofuran_And_Dichloromethane_Delipidation_Of_A_Whole_Mouse_Brain_V1()
    )

    TETRAHYDROFURAN_AND_DICHLOROMETHANE_DELIPIDATION_OF_A_WHOLE_MOUSE_BRAIN_V2 = (
        _Tetrahydrofuran_And_Dichloromethane_Delipidation_Of_A_Whole_Mouse_Brain_V2()
    )

    WHOLE_MOUSE_BRAIN_DELIPIDATION___DICHLOROMETHANE_V1 = _Whole_Mouse_Brain_Delipidation_Dichloromethane_V1()

    WHOLE_MOUSE_BRAIN_DELIPIDATION__IMMUNOLABELING__AND_EXPANSION_MICROSCOPY_V1 = (
        _Whole_Mouse_Brain_Delipidation_Immunolabeling_And_Expansion_Microscopy_V1()
    )

    IMMUNOLABELING_OF_A_WHOLE_MOUSE_BRAIN_V1 = _Immunolabeling_Of_A_Whole_Mouse_Brain_V1()

    STRUCTURAL_MRI_USING_THE_UNIVERSITY_OF_WASHINGTON_14T_VERTICAL_BORE_BRUKER_MRI_V1 = (
        _Structural_Mri_Using_The_University_Of_Washington_14T_Vertical_Bore_Bruker_Mri_V1()
    )

    DURAGEL_APPLICATION_FOR_ACUTE_ELECTROPHYSIOLOGY_RECORDINGS_V1 = (
        _Duragel_Application_For_Acute_Electrophysiology_Recordings_V1()
    )

    SMARTSPIM_SETUP_AND_ALIGNMENT_V1 = _Smartspim_Setup_And_Alignment_V1()

    REFRACTIVE_INDEX_MATCHING___EASYINDEX_V1 = _Refractive_Index_Matching_Easyindex_V1()

    PREPARING_A_3D_PRINTED_IMPLANT_FOR_ACUTE_IN_VIVO_ELECTROPHYSIOLOGY_V1 = (
        _Preparing_A_3D_Printed_Implant_For_Acute_In_Vivo_Electrophysiology_V1()
    )

    IMAGING_CLEARED_MOUSE_BRAINS_ON_SMARTSPIM_V1 = _Imaging_Cleared_Mouse_Brains_On_Smartspim_V1()

    REFRACTIVE_INDEX_MATCHING___ETHYL_CINNAMATE_V1 = _Refractive_Index_Matching_Ethyl_Cinnamate_V1()

    DAPI_STAINING_MOUSE_BRAIN_SECTIONS_V1 = _Dapi_Staining_Mouse_Brain_Sections_V1()

    MODIFIED_FRAME_PROJECTED_INDEPENDENT_FIBER_PHOTOMETRY__FIP__SYSTEM_TRIGGERING_SYSTEM_V1 = (
        _Modified_Frame_Projected_Independent_Fiber_Photometry_Fip_System_Triggering_System_V1()
    )

    MULTI_SITE_OPTIC_FIBER_IMPLANTS_V1 = _Multi_Site_Optic_Fiber_Implants_V1()

    IMMUNOHISTOCHEMISTRY__IHC__STAINING_MOUSE_BRAIN_SECTIONS_V1 = (
        _Immunohistochemistry_Ihc_Staining_Mouse_Brain_Sections_V1()
    )

    SECTIONING_MOUSE_BRAIN_WITH_SLIDING_MICROTOME_V1 = _Sectioning_Mouse_Brain_With_Sliding_Microtome_V1()

    MOUNTING_AND_COVERSLIPPING_MOUSE_BRAIN_SECTIONS_V1 = _Mounting_And_Coverslipping_Mouse_Brain_Sections_V1()

    STEREOTACTIC_INJECTIONS_WITH_HEADFRAME_IMPLANT_V1 = _Stereotactic_Injections_With_Headframe_Implant_V1()

    PROTOCOL_COLLECTION__PERFUSING__SECTIONING__IHC__MOUNTING_AND_COVERSLIPPING_MOUSE_BRAIN_SPECIMENS_V1 = (
        _Protocol_Collection_Perfusing_Sectioning_Ihc_Mounting_And_Coverslipping_Mouse_Brain_Specimens_V1()
    )

    MOUSE_CARDIAC_PERFUSION_FIXATION_AND_BRAIN_COLLECTION_V1 = (
        _Mouse_Cardiac_Perfusion_Fixation_And_Brain_Collection_V1()
    )

    MOUSE_CARDIAC_PERFUSION_FIXATION_AND_BRAIN_COLLECTION_V2 = (
        _Mouse_Cardiac_Perfusion_Fixation_And_Brain_Collection_V2()
    )

    MOUSE_CARDIAC_PERFUSION_FIXATION_AND_BRAIN_COLLECTION_V3 = (
        _Mouse_Cardiac_Perfusion_Fixation_And_Brain_Collection_V3()
    )

    MOUSE_CARDIAC_PERFUSION_FIXATION_AND_BRAIN_COLLECTION_V4 = (
        _Mouse_Cardiac_Perfusion_Fixation_And_Brain_Collection_V4()
    )

    MOUSE_CARDIAC_PERFUSION_FIXATION_AND_BRAIN_COLLECTION_V5 = (
        _Mouse_Cardiac_Perfusion_Fixation_And_Brain_Collection_V5()
    )

    MOUSE_CARDIAC_PERFUSION_FIXATION_AND_BRAIN_COLLECTION_V6 = (
        _Mouse_Cardiac_Perfusion_Fixation_And_Brain_Collection_V6()
    )

    MOUSE_CARDIAC_PERFUSION_FIXATION_AND_BRAIN_COLLECTION_V7 = (
        _Mouse_Cardiac_Perfusion_Fixation_And_Brain_Collection_V7()
    )

    MOUSE_CARDIAC_PERFUSION_FIXATION_AND_BRAIN_COLLECTION_V8 = (
        _Mouse_Cardiac_Perfusion_Fixation_And_Brain_Collection_V8()
    )

    ALL = tuple(ProtocolModel.__subclasses__())

    ONE_OF = Annotated[Union[tuple(ProtocolModel.__subclasses__())], Field(discriminator="title")]

    doi_map = {m().registry_identifier: m() for m in ALL if getattr(m(), "registry_identifier", None)}

    @classmethod
    def from_doi(cls, doi: str) -> ProtocolModel:
        """Return protocol model by DOI."""
        return cls.doi_map.get(doi, None)

    @classmethod
    def from_url(cls, url: str) -> ProtocolModel:
        """Return protocol model by DOI, stripping URL prefixes."""
        # Remove any leading protocol/domain up to the DOI
        doi = re.sub(r"^(https?://)?(dx\.)?doi\.org/", "", url)
        return cls.from_doi(doi)

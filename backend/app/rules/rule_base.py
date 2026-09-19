"""
Structured Rule Base for Construction Waste Recovery Planner.
Defines transparent, explainable IF/THEN rules for all construction materials.
"""

from typing import List, Dict, Any

RULES_DATABASE: List[Dict[str, Any]] = [
    # --- CONCRETE ---
    {
        "rule_id": "C1",
        "material": "Concrete",
        "pathway": "REUSE",
        "priority": 1,
        "conditions_description": "Condition is Excellent or Good AND Contamination is None or Low",
        "reason": "Intact, clean concrete elements retain structural capacity and geometry, enabling direct salvage and reuse without energy-intensive reprocessing.",
        "applications": [
            "New construction",
            "Non-structural elements",
            "Landscaping",
            "Paving",
            "Precast blocks where technically appropriate"
        ],
        "alternatives": ["Recycling into aggregate"],
        "evaluator": lambda c, cont, char: c in ["Excellent", "Good"] and cont in ["None", "Low"]
    },
    {
        "rule_id": "C2",
        "material": "Concrete",
        "pathway": "RECYCLE",
        "priority": 3,
        "conditions_description": "Condition is Moderate or Damaged AND Contamination is None or Low",
        "reason": "Direct reuse is unsuitable due to the material condition, while clean concrete remains suitable for processing into recycled aggregate.",
        "applications": [
            "Recycled aggregate",
            "Road base",
            "Sub-base",
            "Fill material where appropriate"
        ],
        "alternatives": ["Controlled reuse for suitable non-structural applications"],
        "evaluator": lambda c, cont, char: c in ["Moderate", "Damaged"] and cont in ["None", "Low"]
    },
    {
        "rule_id": "C3",
        "material": "Concrete",
        "pathway": "SPECIALIZED DISPOSAL / HANDLING",
        "priority": 5,
        "conditions_description": "Contamination is High or Hazardous (or Severely Damaged with chemical ingress)",
        "reason": "Contamination prevents normal reuse or recycling. Specialized handling, regulatory chemical testing, or certified containment is required.",
        "applications": [
            "Controlled hazardous containment",
            "Pre-treatment and chemical stabilization",
            "Regulated industrial landfill"
        ],
        "alternatives": ["Certified chemical decontamination if verified feasible by laboratory test"],
        "evaluator": lambda c, cont, char: cont in ["High", "Hazardous"] or (c == "Severely Damaged" and cont != "None")
    },

    # --- BRICK ---
    {
        "rule_id": "B1",
        "material": "Brick",
        "pathway": "REUSE",
        "priority": 1,
        "conditions_description": "Condition is Excellent or Good AND Contamination is None or Low AND broken percentage is low",
        "reason": "Clean, intact masonry units retain high mechanical strength and architectural charm, making direct salvage and reuse the most sustainable option.",
        "applications": [
            "Wall construction",
            "Landscaping",
            "Paving",
            "Decorative construction"
        ],
        "alternatives": ["Crushing into decorative brick aggregate"],
        "evaluator": lambda c, cont, char: c in ["Excellent", "Good"] and cont in ["None", "Low"] and (float(char.get("broken_percentage", 0)) <= 25)
    },
    {
        "rule_id": "B2",
        "material": "Brick",
        "pathway": "RECYCLE",
        "priority": 3,
        "conditions_description": "Condition is Damaged/Moderate (or broken > 25%) AND Contamination is None or Low",
        "reason": "Broken or fractured bricks cannot provide structural integrity for whole masonry reuse, but clean brick fragments are highly effective for crushed aggregate.",
        "applications": [
            "Brick aggregate",
            "Fill material",
            "Road base where appropriate",
            "Landscaping groundcover"
        ],
        "alternatives": ["Controlled secondary backfill"],
        "evaluator": lambda c, cont, char: (c in ["Damaged", "Moderate", "Severely Damaged"] or float(char.get("broken_percentage", 0)) > 25) and cont in ["None", "Low"]
    },
    {
        "rule_id": "B3",
        "material": "Brick",
        "pathway": "SPECIALIZED DISPOSAL / HANDLING",
        "priority": 5,
        "conditions_description": "Contamination is High or Hazardous (e.g. hazardous mortar, chemical coatings)",
        "reason": "Hazardous contamination poses chemical migration risks, preventing safe crushing or unconfined fill use.",
        "applications": [
            "Hazardous waste containment facility",
            "Chemical stabilization"
        ],
        "alternatives": ["Chemical abatement under certified environmental controls"],
        "evaluator": lambda c, cont, char: cont in ["High", "Hazardous"]
    },

    # --- STEEL ---
    {
        "rule_id": "S1",
        "material": "Steel",
        "pathway": "REUSE",
        "priority": 1,
        "conditions_description": "Good structural integrity AND Contamination is None or Low (Rust is None or Surface)",
        "reason": "Steel sections that retain their geometric and metallurgical integrity can be directly reused or refabricated with near-zero embodied carbon loss.",
        "applications": [
            "Structural components where certified suitable",
            "Fabrication",
            "Secondary construction",
            "Temporary shoring and support beams"
        ],
        "alternatives": ["High-value scrap recycling"],
        "evaluator": lambda c, cont, char: c in ["Excellent", "Good"] and cont in ["None", "Low"] and char.get("structural_integrity", "Sound") != "Compromised"
    },
    {
        "rule_id": "S2",
        "material": "Steel",
        "pathway": "RECYCLE",
        "priority": 3,
        "conditions_description": "Damaged/deformed OR rust is moderate/heavy, BUT Contamination is None or Low",
        "reason": "Steel can be processed and recovered as scrap. Steel possesses 100% recyclability without structural degradation through electric arc melting.",
        "applications": [
            "Electric arc furnace feedstock",
            "Recycled rebar production",
            "Structural steel profiles",
            "Foundry melting"
        ],
        "alternatives": ["Non-structural brackets and downcycled workshop fabrication"],
        "evaluator": lambda c, cont, char: (c in ["Moderate", "Damaged", "Severely Damaged"] or char.get("structural_integrity") == "Compromised" or char.get("rust_level") in ["Moderate", "Severe"]) and cont in ["None", "Low", "Moderate"]
    },
    {
        "rule_id": "S3",
        "material": "Steel",
        "pathway": "SPECIALIZED DISPOSAL / HANDLING",
        "priority": 5,
        "conditions_description": "Contamination is Hazardous (e.g., toxic lead primer, asbestos encapsulation, radioactive contamination)",
        "reason": "Toxic coatings or industrial chemical residues must undergo certified decontamination prior to melting or scrap processing.",
        "applications": [
            "Certified abatement facility",
            "Controlled hazardous waste handling"
        ],
        "alternatives": ["Abrasive blast decontamination with hazardous dust collection"],
        "evaluator": lambda c, cont, char: cont == "Hazardous"
    },

    # --- WOOD ---
    {
        "rule_id": "W1",
        "material": "Wood",
        "pathway": "REUSE",
        "priority": 1,
        "conditions_description": "Wood is Good/Excellent AND rot = No AND contamination is None or Low",
        "reason": "Sound architectural and dimensional lumber maintains structural strength, allowing direct salvage for framing, furniture, and interior fixtures.",
        "applications": [
            "Furniture",
            "Temporary structures",
            "Interior applications",
            "Panels",
            "Salvaged timber beams"
        ],
        "alternatives": ["Remanufacturing into engineered timber or architectural millwork"],
        "evaluator": lambda c, cont, char: c in ["Excellent", "Good"] and cont in ["None", "Low"] and char.get("rot", "No") in ["No", "None"]
    },
    {
        "rule_id": "W2",
        "material": "Wood",
        "pathway": "RECOVER",
        "priority": 4,
        "conditions_description": "Wood is damaged/moderate BUT not hazardous (no chemical rot treatment, clean fragments)",
        "reason": "Damaged wood cannot guarantee structural integrity for direct reuse, but clean timber fibers are ideal for engineered panels or clean biomass energy.",
        "applications": [
            "Wood products",
            "Particle board and MDF manufacture",
            "Biomass fuel where legally and environmentally appropriate",
            "Garden mulch (unpainted only)"
        ],
        "alternatives": ["Composting (clean unpainted timber only)"],
        "evaluator": lambda c, cont, char: (c in ["Moderate", "Damaged", "Severely Damaged"] or char.get("rot") in ["Surface", "Moderate"]) and cont in ["None", "Low", "Moderate"] and char.get("paint_coating") != "Hazardous Lead/Creosote"
    },
    {
        "rule_id": "W3",
        "material": "Wood",
        "pathway": "SPECIALIZED DISPOSAL / HANDLING",
        "priority": 5,
        "conditions_description": "Wood contains hazardous treatment or contamination (CCA, creosote, lead paint)",
        "reason": "Treated wood with hazardous chemical preservatives releases toxic arsenic, chromium, or carcinogenic volatiles if burned or chipped, requiring regulated disposal.",
        "applications": [
            "Specialized high-temperature hazardous incinerator",
            "Classified landfill containment"
        ],
        "alternatives": ["Regulated hazardous containment cell"],
        "evaluator": lambda c, cont, char: cont == "Hazardous" or char.get("paint_coating") == "Hazardous Lead/Creosote" or char.get("rot") == "Severe" and cont in ["High", "Hazardous"]
    },

    # --- GLASS ---
    {
        "rule_id": "G1",
        "material": "Glass",
        "pathway": "REUSE",
        "priority": 1,
        "conditions_description": "Glass is intact or minimally damaged AND contamination is None or Low",
        "reason": "Intact architectural glazing sheets and window units can be safely dismantled, cleaned, and installed in secondary buildings or greenhouses.",
        "applications": [
            "Windows",
            "Partitions",
            "Decorative applications",
            "Greenhouse glazing"
        ],
        "alternatives": ["Cullet processing for high-grade glass container manufacturing"],
        "evaluator": lambda c, cont, char: c in ["Excellent", "Good"] and cont in ["None", "Low"] and char.get("cracked", "No") in ["No", "False"]
    },
    {
        "rule_id": "G2",
        "material": "Glass",
        "pathway": "RECYCLE",
        "priority": 3,
        "conditions_description": "Glass is broken AND uncontaminated (Contamination None or Low)",
        "reason": "Clean broken glass (cullet) can be melted into new glass products at lower temperatures than raw silica, saving substantial energy and emissions.",
        "applications": [
            "Glass cullet",
            "New glass products",
            "Aggregate applications where appropriate",
            "Fiberglass insulation",
            "Abrasive grit"
        ],
        "alternatives": ["Decorative terrazzo aggregate and filtration media"],
        "evaluator": lambda c, cont, char: (c in ["Moderate", "Damaged", "Severely Damaged"] or char.get("cracked") in ["Yes", "True"]) and cont in ["None", "Low"]
    },
    {
        "rule_id": "G3",
        "material": "Glass",
        "pathway": "SPECIALIZED DISPOSAL / HANDLING",
        "priority": 5,
        "conditions_description": "Glass is contaminated with hazardous sealants, wire mesh, or toxic chemicals",
        "reason": "Non-recyclable composite glass (e.g. PCB-contaminated sealants, leaded glass) disrupts cullet melting and requires controlled handling.",
        "applications": [
            "Regulated hazardous waste cell",
            "Specialized recycling facility with mechanical sealant separator"
        ],
        "alternatives": ["Industrial encapsulation"],
        "evaluator": lambda c, cont, char: cont in ["High", "Hazardous"]
    },

    # --- PLASTIC ---
    {
        "rule_id": "P1",
        "material": "Plastic",
        "pathway": "RECYCLE",
        "priority": 3,
        "conditions_description": "Plastic is relatively clean (Contamination None, Low, or Moderate)",
        "reason": "Sorted construction plastics (PVC conduits, HDPE pipes, EPS insulation) can be granulated, washed, and pelletized into secondary construction materials.",
        "applications": [
            "Plastic products",
            "Construction products",
            "Reprocessed piping and drainage",
            "Plastic lumber and spacers"
        ],
        "alternatives": ["Waste-to-energy recovery in certified facilities"],
        "evaluator": lambda c, cont, char: cont in ["None", "Low", "Moderate"] and c != "Severely Damaged"
    },
    {
        "rule_id": "P2",
        "material": "Plastic",
        "pathway": "SPECIALIZED DISPOSAL / HANDLING",
        "priority": 5,
        "conditions_description": "Plastic is heavily contaminated or hazardous (chemicals, toxic adhesives)",
        "reason": "Heavily contaminated plastics cannot be cleaned economically without severe chemical pollution and must be handled under hazardous waste protocols.",
        "applications": [
            "High-temperature hazardous waste incineration with flue-gas scrubbers",
            "Secure landfill"
        ],
        "alternatives": ["Controlled chemical recycling pilot"],
        "evaluator": lambda c, cont, char: cont in ["High", "Hazardous"] or c == "Severely Damaged"
    },

    # --- GYPSUM / DRYWALL ---
    {
        "rule_id": "Y1",
        "material": "Gypsum",
        "pathway": "RECYCLE",
        "priority": 3,
        "conditions_description": "Gypsum is dry AND uncontaminated (Contamination None or Low)",
        "reason": "Dry gypsum consists of pure calcium sulfate dihydrate, which can be segregated, ground, and repeatedly calcined to produce new plasterboard core.",
        "applications": [
            "New gypsum products and drywall",
            "Reprocessed construction plaster",
            "Agricultural soil conditioner (calcium & sulfate)"
        ],
        "alternatives": ["Cement manufacture retarder additive"],
        "evaluator": lambda c, cont, char: cont in ["None", "Low"] and char.get("moisture", "Dry") != "Wet" and char.get("wet", "No") not in ["Yes", "Wet"]
    },
    {
        "rule_id": "Y2",
        "material": "Gypsum",
        "pathway": "DISPOSAL",
        "priority": 5,
        "conditions_description": "Gypsum is wet OR heavily contaminated",
        "reason": "Wet gypsum decomposing in non-hazardous landfills produces toxic, foul-smelling hydrogen sulfide (H2S) gas, requiring dedicated dry-cell disposal.",
        "applications": [
            "Dedicated monofil landfill cell for gypsum",
            "Controlled waste drying and sorting facility"
        ],
        "alternatives": ["Thermal drying followed by mechanical sorting if economically feasible"],
        "evaluator": lambda c, cont, char: cont in ["Moderate", "High", "Hazardous"] or char.get("moisture") == "Wet" or char.get("wet") in ["Yes", "Wet"]
    },

    # --- ASPHALT ---
    {
        "rule_id": "A1",
        "material": "Asphalt",
        "pathway": "RECYCLE",
        "priority": 3,
        "conditions_description": "Asphalt is uncontaminated (Contamination None or Low)",
        "reason": "Reclaimed asphalt pavement (RAP) retains its high-value bituminous binder and hard mineral aggregate, saving both bitumen and virgin rock quarrying.",
        "applications": [
            "Reclaimed asphalt pavement (RAP)",
            "Road construction",
            "Hot-mix and warm-mix asphalt layers",
            "Aggregate sub-base"
        ],
        "alternatives": ["Cold in-place recycling (CIR) for secondary roadways"],
        "evaluator": lambda c, cont, char: cont in ["None", "Low"]
    },
    {
        "rule_id": "A2",
        "material": "Asphalt",
        "pathway": "SPECIALIZED DISPOSAL / HANDLING",
        "priority": 5,
        "conditions_description": "Asphalt has High or Hazardous contamination (coal tar, chemical spills)",
        "reason": "Historic asphalt containing toxic coal tar binders emits carcinogenic polycyclic aromatic hydrocarbons (PAHs) when heated, prohibiting standard recycling.",
        "applications": [
            "Cold stabilization in sealed containment",
            "Hazardous industrial disposal facility"
        ],
        "alternatives": ["Thermal desorption treatment"],
        "evaluator": lambda c, cont, char: cont in ["High", "Hazardous"] or char.get("coal_tar") in ["Yes", "True"]
    },

    # --- SOIL ---
    {
        "rule_id": "SO1",
        "material": "Soil",
        "pathway": "REUSE",
        "priority": 1,
        "conditions_description": "Soil is clean (Contamination None or Low) AND suitable condition",
        "reason": "Clean excavated subsoil and topsoil should be preserved as critical natural capital for engineering fill, site balance, or regional landscaping.",
        "applications": [
            "Landscaping",
            "Backfilling",
            "Site grading",
            "Earthen embankment stabilization"
        ],
        "alternatives": ["Topsoil conditioning and soil blending for community parks"],
        "evaluator": lambda c, cont, char: cont in ["None", "Low"] and c in ["Excellent", "Good", "Moderate"]
    },
    {
        "rule_id": "SO2",
        "material": "Soil",
        "pathway": "SPECIALIZED DISPOSAL / HANDLING",
        "priority": 5,
        "conditions_description": "Soil is contaminated (Contamination Moderate, High, or Hazardous)",
        "reason": "Contaminated soil containing hydrocarbons, heavy metals, or construction solvents threatens groundwater aquifers and requires licensed soil remediation.",
        "applications": [
            "Ex-situ bioremediation facility",
            "Soil washing and thermal desorption plant",
            "Certified hazardous containment cell"
        ],
        "alternatives": ["On-site soil stabilization and encapsulation under regulatory supervision"],
        "evaluator": lambda c, cont, char: cont in ["Moderate", "High", "Hazardous"] or c == "Severely Damaged"
    },

    # --- CERAMIC / TILES ---
    {
        "rule_id": "T1",
        "material": "Ceramic / Tiles",
        "pathway": "REUSE",
        "priority": 1,
        "conditions_description": "Tiles are intact AND clean (Contamination None or Low)",
        "reason": "Intact architectural ceramic, porcelain, and quarry tiles can be cleaned and relaid, maintaining high aesthetic and functional value.",
        "applications": [
            "Flooring",
            "Wall applications",
            "Decorative use",
            "Mosaic and architectural restoration"
        ],
        "alternatives": ["Crushing into premium terrazzo aggregate"],
        "evaluator": lambda c, cont, char: c in ["Excellent", "Good"] and cont in ["None", "Low"] and (float(char.get("intact_percentage", 100)) >= 70)
    },
    {
        "rule_id": "T2",
        "material": "Ceramic / Tiles",
        "pathway": "RECYCLE",
        "priority": 3,
        "conditions_description": "Tiles are broken AND clean (Contamination None or Low)",
        "reason": "Broken ceramic materials possess excellent hardness and chemical inertia, making them great substitutes for natural gravel in aggregates and landscaping.",
        "applications": [
            "Aggregate",
            "Landscaping",
            "Decorative material",
            "Sub-base road drainage"
        ],
        "alternatives": ["Drainage aggregate for storm water swales"],
        "evaluator": lambda c, cont, char: (c in ["Moderate", "Damaged", "Severely Damaged"] or float(char.get("intact_percentage", 100)) < 70) and cont in ["None", "Low"]
    },
    {
        "rule_id": "T3",
        "material": "Ceramic / Tiles",
        "pathway": "SPECIALIZED DISPOSAL / HANDLING",
        "priority": 5,
        "conditions_description": "Tiles contaminated with hazardous asbestos adhesive or lead-rich glaze",
        "reason": "Historic tile adhesives frequently contain asbestos fibers, mandating specialized abatement before disposal.",
        "applications": [
            "Hazardous asbestos-rated disposal facility",
            "Regulated disposal site"
        ],
        "alternatives": ["Controlled encapsulation"],
        "evaluator": lambda c, cont, char: cont in ["High", "Hazardous"]
    },

    # --- MIXED CONSTRUCTION WASTE ---
    {
        "rule_id": "M1",
        "material": "Mixed Construction Waste",
        "pathway": "RECOVER",
        "priority": 4,
        "conditions_description": "Mixed rubble is relatively uncontaminated and suitable for sorting",
        "reason": "Commingled construction debris can be processed through automated Materials Recovery Facilities (MRFs) with trommels and magnets to extract clean mineral and metal fractions.",
        "applications": [
            "Materials Recovery Facility (MRF) mechanical sorting",
            "Crushed mixed aggregate for non-structural fill",
            "Recovered scrap metal separation",
            "Refuse-derived fuel (RDF) for high-calorific non-recyclable fractions"
        ],
        "alternatives": ["Engineered backfill under regulatory permit"],
        "evaluator": lambda c, cont, char: cont in ["None", "Low", "Moderate"] and char.get("separable_on_site", "Yes") in ["Yes", "True"]
    },
    {
        "rule_id": "M2",
        "material": "Mixed Construction Waste",
        "pathway": "DISPOSAL",
        "priority": 5,
        "conditions_description": "Mixed waste is heavily contaminated or unsegregable",
        "reason": "Unsegregable contaminated mixed waste poses high cross-contamination risks and cannot be processed safely into secondary materials.",
        "applications": [
            "Licensed sanitary landfill",
            "Controlled waste transfer station"
        ],
        "alternatives": ["Secondary mechanical sorting if contamination can be isolated"],
        "evaluator": lambda c, cont, char: cont in ["High", "Hazardous"] or char.get("separable_on_site") in ["No", "False"]
    }
]

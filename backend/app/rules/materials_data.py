"""
Materials Knowledge Base data for Construction Waste Recovery Planner.
"""

from typing import List, Dict, Any

MATERIALS_DATABASE: List[Dict[str, Any]] = [
    {
        "name": "Concrete",
        "category": "Mineral / Inert",
        "description": "Concrete is the most voluminous construction material globally, composed of Portland cement, water, fine aggregate (sand), and coarse aggregate (gravel or crushed stone).",
        "typical_waste_source": "Demolition of reinforced concrete frames, slabs, foundations, precast structural elements, and testing cubes.",
        "reuse_potential": "High for undamaged precast modular units, panels, pavers, and retaining wall blocks.",
        "recycling_potential": "Very High. Clean concrete can be crushed into Recycled Concrete Aggregate (RCA) to replace virgin quarry aggregate in road base and non-structural mixes.",
        "common_applications": [
            "Recycled concrete aggregate (RCA)",
            "Road sub-base and structural fill",
            "Permeable gravel paving",
            "Precast retaining wall units"
        ],
        "important_considerations": "Chemical contamination (chlorides, sulfates, hydrocarbons) or structural cracking must be evaluated. Clean rebar must be separated using magnetic extraction."
    },
    {
        "name": "Brick",
        "category": "Ceramic / Masonry",
        "description": "Kiln-fired clay bricks and calcium silicate bricks used primarily in exterior facades, interior partition walls, and decorative landscaping.",
        "typical_waste_source": "Building alterations, wall demolitions, chimney tear-downs, excess site cuttings.",
        "reuse_potential": "Very High for intact heritage and contemporary bricks when lime mortar allows easy cleaning without face damage.",
        "recycling_potential": "High. Damaged or fractured bricks are crushed into brick dust, sub-base aggregate, and decorative red horticultural gravel.",
        "common_applications": [
            "Architectural masonry facade reuse",
            "Paving and garden landscaping",
            "Crushed brick sub-base aggregate",
            "Tennis court surfacing and decorative mulch"
        ],
        "important_considerations": "Modern hard Portland cement mortar can make deconstruction difficult without fracturing the brick face. Mortar friability and contamination must be evaluated."
    },
    {
        "name": "Steel",
        "category": "Ferrous Metal",
        "description": "High-strength ferrous alloy widely deployed in structural columns, beams (I-beams, H-sections), corrugated roof sheets, and concrete reinforcement rebar.",
        "typical_waste_source": "Demolition of structural frames, industrial warehouses, reinforcement cut-offs, steel studs.",
        "reuse_potential": "Very High. Uncompromised structural sections can be certified, refabricated, and reinstalled with tremendous embodied carbon savings.",
        "recycling_potential": "Exceptional (100%). Steel maintains infinite recyclability through electric arc furnace (EAF) remelting without metallurgical degradation.",
        "common_applications": [
            "Direct structural beam and column reuse",
            "Electric arc furnace remelt into reinforcement bar",
            "Prefabricated workshop trusses and brackets",
            "Steel sheet cladding"
        ],
        "important_considerations": "Check for yield strength, fatigue history, corrosion depth, and hazardous lead-based primer coats from older structures."
    },
    {
        "name": "Wood",
        "category": "Bio-based / Organic",
        "description": "Natural and engineered timber framing, softwood joists, plywood sheets, glulam beams, hardwood floorboards, and temporary formwork panels.",
        "typical_waste_source": "Roof trusses, floor joists, formwork stripping, framing demolition, interior renovations.",
        "reuse_potential": "High for clean, unrotted architectural timber, antique hardwood floors, and heavy timber posts.",
        "recycling_potential": "Moderate to High. Damaged clean wood can be chipped for particle board, medium-density fibreboard (MDF), or clean biomass energy.",
        "common_applications": [
            "Architectural furniture and decorative panelling",
            "Secondary framing and temporary site hoarding",
            "Engineered wood composites and chipboard",
            "Clean biomass combustion (clean wood only)"
        ],
        "important_considerations": "Critically inspect for fungal dry rot, insect infestation, and hazardous chemical preservatives such as Chromated Copper Arsenate (CCA) or Creosote."
    },
    {
        "name": "Glass",
        "category": "Mineral / Silicate",
        "description": "Soda-lime-silica flat architectural glazing, double-glazed sealed units, tempered safety glass, and interior partitions.",
        "typical_waste_source": "Window replacement retrofits, commercial curtain wall renovations, interior partition dismantling.",
        "reuse_potential": "Moderate for intact standard double-glazed units and modular partition panels.",
        "recycling_potential": "High. Clean cullet melts at 20-30% lower temperature than raw virgin sand, providing immediate carbon and energy reductions.",
        "common_applications": [
            "Direct window and greenhouse glazing",
            "Glass cullet for new container and flat glass",
            "Fiberglass thermal insulation",
            "Abrasive blasting media and terrazzo aggregate"
        ],
        "important_considerations": "Avoid mixing flat window glass with ceramic or borosilicate cookware glass. Inspect for hazardous polychlorinated biphenyl (PCB) sealants in pre-1980 glazing."
    },
    {
        "name": "Plastic",
        "category": "Polymer / Synthetic",
        "description": "Thermoplastic polymers including PVC (conduits, pipes, window profiles), HDPE (drainage pipes), and EPS/XPS (rigid insulation foams).",
        "typical_waste_source": "Plumbing retrofits, conduit cut-offs, packaging wrapping, demolition of insulation panels.",
        "reuse_potential": "Moderate for undamaged rigid pipes, fittings, and inspection chambers.",
        "recycling_potential": "High for sorted, uncontaminated mono-polymer streams (especially HDPE and unplasticized PVC).",
        "common_applications": [
            "Recycled drainage and underground cable conduits",
            "Composite plastic lumber and decking",
            "Temporary road mats and pipe spacers",
            "Secondary construction accessories"
        ],
        "important_considerations": "Polymer identification is vital. Cross-contamination between incompatible plastics prevents quality remoulding. Heavy dirt or adhesive must be washed."
    },
    {
        "name": "Gypsum",
        "category": "Mineral / Sulfate",
        "description": "Hydrated calcium sulfate sheet material sandwiched between heavy paper facers, commonly used as interior drywall, plasterboard, and ceiling lining.",
        "typical_waste_source": "Drywall partition tear-outs, offcuts from new interior construction, ceiling renovations.",
        "reuse_potential": "Low for demolished boards due to screw damage, but large offcuts can be salvaged for small patching.",
        "recycling_potential": "Very High. Gypsum core is 100% recyclable infinitely through mechanical paper separation and calcination.",
        "common_applications": [
            "Closed-loop manufacture of new gypsum wallboards",
            "Agricultural soil amendment (calcium & sulfate nutrient source)",
            "Cement manufacturing setting-time retarder"
        ],
        "important_considerations": "Gypsum MUST be kept dry. In wet, anaerobic landfill conditions, sulfate-reducing bacteria convert gypsum into toxic, foul hydrogen sulfide (H2S) gas."
    },
    {
        "name": "Asphalt",
        "category": "Bituminous / Hydrocarbon",
        "description": "Composite mixture of mineral aggregate, filler, and petroleum-derived bitumen binder used in flexible pavements, driveways, and roofing membranes.",
        "typical_waste_source": "Road milling, pavement resurfacing, trench excavations for utilities, parking lot reconstructions.",
        "reuse_potential": "Moderate for intact asphalt paving slabs.",
        "recycling_potential": "Exceptional (up to 100%). Reclaimed Asphalt Pavement (RAP) is one of the most widely recycled materials by weight on Earth.",
        "common_applications": [
            "Hot-mix and warm-mix asphalt pavement with RAP",
            "Cold in-place recycling (CIR) for regional roads",
            "Stabilized base and sub-base layers",
            "Unpaved shoulder paving"
        ],
        "important_considerations": "Older asphalt laid prior to the 1980s may contain coal tar, which contains high polycyclic aromatic hydrocarbons (PAHs) requiring specialized handling."
    },
    {
        "name": "Soil",
        "category": "Geotechnical / Natural",
        "description": "Excavated topsoil, subsoil, clay, and naturally occurring geological sands produced during groundwork and foundation digging.",
        "typical_waste_source": "Basement excavation, trenching, foundation digging, site grading.",
        "reuse_potential": "Very High. Cut-and-fill balancing on-site or direct transfer to nearby civil infrastructure projects.",
        "recycling_potential": "Moderate. Can be screened, blended with organic compost, and converted to certified landscaping topsoil.",
        "common_applications": [
            "On-site cut-and-fill balance",
            "Engineered structural backfill",
            "Landscaping, park development, and agricultural restoration",
            "Earthen flood defense berms"
        ],
        "important_considerations": "Must verify that soil is free from industrial chemical spills, heavy metals, pesticides, or construction debris through geotechnical testing."
    },
    {
        "name": "Ceramic / Tiles",
        "category": "Vitrified Mineral",
        "description": "Glazed and unglazed ceramic tiles, vitrified porcelain floor tiles, terra cotta roof tiles, and quarry tiles.",
        "typical_waste_source": "Bathroom and kitchen renovations, floor stripping, roof repairs.",
        "reuse_potential": "High for intact vintage tiles, terra cotta roof tiles, and carefully salvaged porcelain pavers.",
        "recycling_potential": "High. Crushed ceramics are chemically inert, hard, and frost-resistant, making them ideal aggregates.",
        "common_applications": [
            "Architectural floor and wall relaid tiles",
            "Decorative terrazzo flooring aggregate",
            "Permeable gravel pathways and water swales",
            "Engineered sub-base aggregate"
        ],
        "important_considerations": "Check for legacy asbestos-containing mastic adhesives on older floor tiles. Tiles with tenacious cement mortar are best routed to crushing."
    },
    {
        "name": "Mixed Construction Waste",
        "category": "Composite / Commingled",
        "description": "Unsorted mixture of masonry rubble, packaging, metals, plastics, plaster, and timber typically generated in small site skips and fast demolitions.",
        "typical_waste_source": "Skip waste from residential remodels, rapid site clearances, demolition of multi-material partitions.",
        "reuse_potential": "Low without extensive sorting.",
        "recycling_potential": "Moderate. High-efficiency automated Materials Recovery Facilities (MRFs) can recover up to 70-85% by weight through mechanical sorting.",
        "common_applications": [
            "MRF mechanical sorting into recovered metals and crushed rubble",
            "Non-structural engineered fill",
            "Refuse-derived fuel (RDF) for high-calorific fraction",
            "Daily landfill cover"
        ],
        "important_considerations": "On-site source segregation is always superior to commingled waste. Hazardous substances (paints, batteries, chemicals) must be strictly isolated."
    }
]

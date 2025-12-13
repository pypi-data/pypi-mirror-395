from enum import Enum


class BallastCapacityPortCallsSources(Enum):
    """"""

    Forecast = "Forecast"  #:
    Market = "Market"  #:
    AIS = "AIS"  #:
    Port = "Port"  #:
    Analyst = "Analyst"  #:
    Fixture = "Fixture"  #:


class BallastCapacityPortCallsVesselStates(Enum):
    """"""

    Ballast = "Ballast"  #:
    Loaded = "Loaded"  #:


class BallastCapacitySeriesPeriod(Enum):
    """"""

    Monthly = "monthly"  #:
    Weekly = "weekly"  #:
    Daily = "daily"  #:


class BallastCapacitySeriesSplit(Enum):
    """"""

    Total = "total"  #:
    Country = "country"  #:
    Source = "source"  #:
    VesselType = "vesselType"  #:
    VesselTypeCpp = "vesselTypeCpp"  #:
    VesselTypeOil = "vesselTypeOil"  #:


class BallastCapacitySeriesUnit(Enum):
    """"""

    MT = "mt"  #:
    KT = "kt"  #:


class BallastCapacitySeriesMetric(Enum):
    """"""

    Count = "count"  #:
    DeadWeight = "deadWeight"  #:
    Capacity = "capacity"  #:


class CongestionSeriesPeriod(Enum):
    """"""

    Annually = "years"  #:
    Monthly = "months"  #:
    Weekly = "weeks"  #:
    Quarterly = "quarters"  #:
    Daily = "days"  #:
    EIA = "eia"  #:


class CongestionVesselsPeriod(Enum):
    """"""

    Annually = "years"  #:
    Monthly = "months"  #:
    Weekly = "weeks"  #:
    Quarterly = "quarters"  #:
    Daily = "days"  #:
    EIA = "eia"  #:


class CongestionSeriesSplit(Enum):
    """"""

    Total = "total"  #:
    Port = "port"  #:
    Installation = "installation"  #:
    Country = "country"  #:
    VesselType = "vesselType"  #:
    VesselTypeCpp = "vesselTypeCpp"  #:
    VesselTypeOil = "vesselTypeOil"  #:
    VesselOperations = "VesselOperations"  #:
    WaitingStatus = "waitingStatus"  #:
    Product = "product"  #:
    Grade = "grade"  #:


class CongestionSeriesUnit(Enum):
    """"""

    MT = "mt"  #:
    KT = "kt"  #:


class CongestionSeriesMetric(Enum):
    """"""

    Count = "count"  #:
    DeadWeight = "deadWeight"  #:
    Duration = "duration"  #:
    Capacity = "capacity"  #:


class CongestionSeriesOperation(Enum):
    """"""

    Load = "Load"  #:
    Discharge = "Discharge"  #:
    All = "All"  #:


class CongestionVesselsOperation(Enum):
    """"""

    Load = "Load"  #:
    Discharge = "Discharge"  #:
    All = "All"  #:


class Platform(Enum):
    """"""

    LNG = "https://api-lng.kpler.com/v1"  #:
    LPG = "https://api-lpg.kpler.com/v1"  #:
    Dry = "https://api-coal.kpler.com/v1"  #:
    Liquids = "https://api.kpler.com/v1"  #:


class TradesStatus(Enum):
    """"""

    Delivered = "delivered"  #:
    Scheduled = "scheduled"  #:
    Loading = "loading"  #:
    InTransit = "in transit"  #:


class FleetDevelopmentSeriesAggregationMetric(Enum):
    """"""

    Count = "count"  #:
    SumCapacity = "sumcapacity"  #:
    SumDeadWeight = "sumdeadweight"  #:


class FleetDevelopmentSeriesMetric(Enum):
    """"""

    Available = "available"  #:
    Deliveries = "deliveries"  #:
    Scrapping = "scrapping"  #:
    Contracting = "contracting"  #:


class FleetDevelopmentSeriesPeriod(Enum):
    """"""

    Annually = "years"  #:
    Monthly = "months"  #:
    Quarterly = "quarters"  #:


class FleetDevelopmentSeriesSplit(Enum):
    """"""

    Total = "total"  #:
    ComplianceMethod = "complianceMethod"  #:
    VesselType = "vesselType"  #:
    VesselTypeOil = "vesselTypeOil"  #:
    VesselTypeCpp = "vesselTypeCpp"  #:


class FleetDevelopmentSeriesUnit(Enum):
    """"""

    MT = "mt"  #:
    KT = "kt"  #:


class FlowsDirection(Enum):
    """"""

    Import = "import"  #:
    Export = "export"  #:
    NetImport = "netimport"  #:
    NetExport = "netexport"  #:


class FlowsSplit(Enum):
    """"""

    Total = "total"  #:
    Grades = "grades"  #:
    Products = "products"  #:
    OriginCountries = "origin countries"  #:
    OriginSubcontinents = "origin subcontinents"  #:
    OriginContinents = "origin continents"  #:
    OriginTradingRegions = "origin trading regions"  #:
    OriginPorts = "origin ports"
    DestinationTradingRegions = "destination trading regions"  #:
    DestinationCountries = "destination countries"  #:
    DestinationSubcontinents = "destination subcontinents"  #:
    DestinationContinents = "destination continents"  #:
    OriginInstallations = "origin installations"  #:
    DestinationInstallations = "destination installations"  #:
    DestinationPorts = "destination ports"
    OriginPadds = "origin padds"  #:
    DestinationPadds = "destination padds"  #:
    VesselType = "vessel type"  #:
    TradeStatus = "trade status"  #:
    Sources = "sources"  #:
    Charterers = "charterers"  #:
    Routes = "routes"  #:
    Buyers = "buyer"  #:
    Sellers = "seller"  #:
    VesselTypeOil = "vessel type oil"  #:
    VesselTypeCpp = "vessel type cpp"  #:
    LongHaulVesselType = "long haul vessel type"  #:
    LongHaulVesselTypeOil = "long haul vessel type oil"  #:
    LongHaulVesselTypeCpp = "long haul vessel type cpp"  #:
    CrudeQuality = "crude quality"  #:


class FlowsPeriod(Enum):
    """"""

    Annually = "annually"  #:
    Monthly = "monthly"  #:
    Weekly = "weekly"  #:
    EiaWeekly = "eia-weekly"  #:
    Daily = "daily"  #:


class FlowsMeasurementUnit(Enum):
    """"""

    KBD = "kbd"  #:
    BBL = "bbl"  #:
    KB = "kb"  #:
    MMBBL = "mmbbl"  #:
    MT = "mt"  #:
    KT = "kt"  #:
    T = "t"  #:
    CM = "cm"  #:


class FreightMetricsSeriesMetric(Enum):
    """"""

    TonMiles = "TonMiles"  #:
    TonDays = "TonDays"  #:
    AvgSpeed = "AvgSpeed"  #:
    AvgDistance = "AvgDistance"  #:


class FreightMetricsSeriesPeriod(Enum):
    """"""

    Monthly = "monthly"  #:
    Quarterly = "quarterly"  #:
    Annually = "annually"  #:


class FreightMetricsSeriesSplit(Enum):
    """"""

    Total = "total"  #:
    DestinationCountry = "destinationCountry"  #:
    OriginCountry = "originCountry"  #:
    VesselType = "vesselType"  #:
    VesselTypeOil = "vesselTypeOil"  #:
    VesselTypeCpp = "vesselTypeCpp"  #:
    DestinationInstallation = "destinationInstallation"  #:
    OriginInstallation = "originInstallation"  #:
    DestinationSourceEta = "destinationSourceEta"  #:
    OriginSourceEta = "originSourceEta"  #:


class FreightMetricsSeriesUnit(Enum):
    """"""

    MTNMI = "mt/nmi"  #:
    KTNMI = "kt/nmi"  #:
    TNMI = "t/nmi"  #:
    TDAY = "t/day"  #:
    KTDAY = "kt/day"  #:


class FreightMetricsSeriesStatus(Enum):
    """Status of vessels for freight metrics series"""

    Ballast = "ballast"  #:
    Loaded = "loaded"  #:
    All = "all"  #:


class VesselTypesDry(Enum):
    """"""

    BabyCapes = "Baby Capes"  #:
    Capesize = "Capesize"  #:
    Handymax = "Handymax"  #:
    Handysize = "Handysize"  #:
    Newcastlemax = "Newcastlemax"  #:
    Kamsarmax = "Kamsarmax"  #:
    Panamax = "Panamax"  #:
    PostPanamax = "Post-Panamax"  #:
    Supramax = "Supramax"  #:
    Ultramax = "Ultramax"  #:
    Valemax = "Valemax"  #:
    VLOC = "VLOC"  #:


class VesselTypesLPG(Enum):
    """"""

    SGC = "SGC"  #:
    VLGC = "VLGC"  #:
    Handysize = "Handysize"  #:
    MGC = "MGC"  #:
    LGC = "LGC"  #:
    VLEC = "VLEC"  #:


class VesselTypesLNG(Enum):
    """"""

    XLUpperConventional = "XL (Upper Conventional)"  #:
    LLowerConventional = "L (Lower Conventional)"  #:
    QFlex = "Q-Flex"  #:
    XSPressureGas = "XS (Pressure Gas)"  #:
    MMedMax = "M (Med Max)"  #:
    SSmallSCale = "S (Small Scale)"  #:
    QMax = "Q-Max"  #:


class VesselTypesCPP(Enum):
    """"""

    LR2 = "LR2"  #:
    VLCC = "VLCC"  #:
    LR3 = "LR3"  #:
    MR = "MR"  #:
    GP = "GP"  #:
    LR1 = "LR1"  #:
    SmallTanker = "Small Tanker"  #:


class VesselTypesOil(Enum):
    """"""

    Aframax = "Aframax"  #:
    ProductTanker = "Product Tanker"  #:
    Suezmax = "Suezmax"  #:
    VLCC = "VLCC"  #:
    Panamax = "Panamax"  #:
    ULCC = "ULCC"  #:
    SmallTanker = "Small Tanker"  #:


class TonnageSupplyVesselTypes(Enum):
    """Vessel types for Tonnage Supply endpoints (cross-platform)"""

    # Dry
    BabyCapes = "Baby Capes"  #:
    Capesize = "Capesize"  #:
    Handymax = "Handymax"  #:
    Handysize = "Handysize"  #:
    MiniBulker = "Mini Bulker"  #:
    Newcastlemax = "Newcastlemax"  #:
    Kamsarmax = "Kamsarmax"  #:
    Panamax = "Panamax"  #:
    PostPanamax = "Post-Panamax"  #:
    Supramax = "Supramax"  #:
    Ultramax = "Ultramax"  #:
    Valemax = "Valemax"  #:
    VLOC = "VLOC"  #:
    # Liquids
    VLCC = "VLCC"  #:
    SuezmaxLR3 = "Suezmax/LR3"  #:
    AframaxLR2 = "Aframax/LR2"  #:
    PanamaxLR1 = "Panamax/LR1"  #:
    MR = "MR"  #:
    HandyMR1 = "Handy/MR1"  #:
    IntermediateTankers = "Intermediate Tankers"  #:
    ShortSeaTankers = "Short Sea Tankers"  #:
    SmallTankers = "Small Tankers"  #:
    # LNG
    QMax = "Q-Max"  #:
    QFlex = "Q-Flex"  #:
    UpperConventional = "Upper Conventional"  #:
    MidConventional = "Mid Conventional"  #:
    LowerConventional = "Lower Conventional"  #:
    MidScale = "Mid-Scale"  #:
    SmallScale = "Small-Scale"  #:
    LargeScaleFloater = "Large-Scale Floater"  #:
    # LPG
    SGC = "SGC"  #:
    VLGC = "VLGC"  #:
    Handy = "Handy"  #:
    MGC = "MGC"  #:
    LGC = "LGC"  #:
    VLEC = "VLEC"  #:
    VLAC = "VLAC"  #:


class TonnageSupplyVesselsState(Enum):
    """Vessel states for Tonnage Supply endpoints"""

    Ballast = "Ballast"  #:
    Loaded = "Loaded"  #:
    Maintenance = "Maintenance"  #:
    Other = "Other"  #:


class TonnageSupplySeriesMetric(Enum):
    """Metrics for Tonnage Supply Series endpoint"""

    Count = "count"  #:
    DeadWeight = "deadWeight"  #:
    Capacity = "capacity"  #:


class TonnageSupplySeriesSplit(Enum):
    """Split options for Tonnage Supply Series endpoint"""

    Total = "total"  #:
    Product = "product"  #:
    State = "state"  #:
    VesselType = "vesselType"  #:
    CurrentContinents = "currentContinents"  #:
    CurrentSubcontinents = "currentSubcontinents"  #:
    CurrentCountries = "currentCountries"  #:
    CurrentSubregions = "currentSubregions"  #:
    CurrentSeas = "currentSeas"  #:
    SubState = "subState"  #:
    Direction = "direction"  #:
    PreviousTradingRegions = "previousTradingRegions"  #:
    PreviousContinents = "previousContinents"  #:
    PreviousSubContinents = "previousSubContinents"  #:
    PreviousCountries = "previousCountries"  #:
    PreviousPorts = "previousPorts"  #:
    NextTradingRegions = "nextTradingRegions"  #:
    NextContinents = "nextContinents"  #:
    NextSubContinents = "nextSubContinents"  #:
    NextCountries = "nextCountries"  #:
    NextPorts = "nextPorts"  #:


class FleetDevelopmentVesselsComplianceMethods(Enum):
    """"""

    Scrubber = "Scrubber"  #:
    ScrubberPlanned = "Scrubber Planned"  #:
    ScrubberReady = "Scrubber Ready"  #:


class FleetDevelopmentVesselsMetric(Enum):
    """"""

    Available = "available"  #:
    Deliveries = "deliveries"  #:
    Scrapping = "scrapping"  #:
    Contracting = "contracting"  #:


class FleetMetricsAlgo(Enum):
    """"""

    FloatingStorage = "floating_storage"  #:
    LoadedVessels = "loaded_vessels"  #:


class FleetMetricsPeriod(Enum):
    """"""

    Weekly = "weekly"  #:
    Daily = "daily"  #:
    EIA = "eia"  #:


class FleetMetricsMeasurementUnit(Enum):
    """"""

    BBL = "bbl"  #:
    T = "t"  #:
    CM = "cm"  #:


class FleetMetricsSplit(Enum):
    """"""

    Total = "total"  #:
    Grades = "grades"  #:
    Products = "products"  #:
    OriginCountries = "origin countries"  #:
    OriginTradingRegions = "origin trading regions"
    DestinationTradingRegions = "destination trading regions"
    OriginContinents = "origin continents"
    OriginSubcontinents = "origin subcontinents"
    DestinationSubcontinents = "destination subcontinents"
    OriginPorts = "origin ports"
    DestinationPorts = "destination ports"
    DestinationContinents = "destination continents"
    DestinationCountries = "destination countries"  #:
    OriginInstallations = "origin installations"  #:
    DestinationInstallations = "destination installations"  #:
    VesselType = "vessel type"  #:
    VesselTypeOil = "vessel type oil"
    VesselTypeCpp = "vessel type cpp"
    TradeStatus = "trade status"  #:
    Charterers = "charterers"  #:
    Buyer = "buyer"  #:
    Seller = "seller"  #:
    CurrentContinents = "current continents"  #:
    CurrentSubcontinents = "current subcontinents"  #:
    CurrentCountries = "current countries"  #:
    CurrentSubregions = "current subregions"  #:
    CurrentSeas = "current seas"  #:
    FloatingDays = "floating days"  #:
    CrudeQuality = "crude quality"  #:


class FleetMetricsVesselsAlgo(Enum):
    """"""

    FloatingStorage = "floating_storage"  #:
    LoadedVessels = "loaded_vessels"  #:


class FleetMetricsVesselsMeasurementUnit(Enum):
    """"""

    BBL = "bbl"  #:
    KB = "kb"  #:
    MMBBL = "mmbbl"  #:
    MT = "mt"  #:
    KT = "kt"  #:
    T = "t"  #:
    CM = "cm"  #:


class OutagesTypes(Enum):
    """"""

    Planned = "planned"  #:
    Unplanned = "unplanned"  #:


class ContractsTypes(Enum):
    """"""

    SPA = "SPA"  #:
    TUA = "TUA"  #:
    LTA = "LTA"  #:
    Tender = "Tender"  #:


class FleetUtilizationSeriesPeriod(Enum):
    """"""

    Annually = "years"  #:
    Monthly = "months"  #:
    Weekly = "weeks"  #:
    Quarterly = "quarters"  #:
    Daily = "days"  #:


class FleetUtilizationVesselsPeriod(Enum):
    """"""

    Annually = "years"  #:
    Monthly = "months"  #:
    Weekly = "weeks"  #:
    Quarterly = "quarters"  #:
    Daily = "days"  #:


class FleetUtilizationSeriesSplit(Enum):
    """"""

    Total = "total"  #:
    Product = "product"  #:
    State = "state"  #:
    VesselType = "vesselType"  #:
    VesselTypeOil = "vesselTypeOil"  #:
    VesselTypeCpp = "vesselTypeCpp"  #:
    SubState = "subState"  #:
    Direction = "direction"  #:
    CurrentSubContinents = "currentSubcontinents"  #:
    CurrentContinents = "currentContinents"  #:
    CurrentSubregions = "currentSubregions"  #:
    CurrentCountries = "currentCountries"  #:
    CurrentSeas = "currentSeas"  #:
    PreviousTradingRegions = "previousTradingRegions"  #:
    PreviousContinents = "previousContinents"  #:
    PreviousSubContinents = "previousSubContinents"  #:
    PreviousCountries = "previousCountries"  #:
    PreviousPorts = "previousPorts"  #:
    NextTradingRegions = "nextTradingRegions"  #:
    NextContinents = "nextContinents"  #:
    NextSubContinents = "nextSubContinents"  #:
    NextCountries = "nextCountries"  #:
    NextPorts = "nextPorts"  #:


class FleetUtilizationSeriesUnit(Enum):
    """"""

    MT = "mt"  #:
    KT = "kt"  #:


class FleetUtilizationSeriesVesselsState(Enum):
    """"""

    Ballast = "Ballast"  #:
    Loaded = "Loaded"  #:
    Maintenance = "Maintenance"  #:


class FleetUtilizationSeriesMetric(Enum):
    """"""

    Count = "count"  #:
    DeadWeight = "deadWeight"  #:


class FleetUtilizationVesselsState(Enum):
    """"""

    Ballast = "Ballast"  #:
    Loaded = "Loaded"  #:
    Maintenance = "Maintenance"  #:


class FleetUtilizationVesselsUnit(Enum):
    """"""

    MT = "mt"  #:
    KT = "kt"  #:


class InventoriesPeriod(Enum):
    """"""

    Annually = "annually"  #:
    Monthly = "monthly"  #:
    Weekly = "weekly"  #:
    EiaWeekly = "eia-weekly"  #:
    Daily = "daily"  #:


class InventoriesSplit(Enum):
    """"""

    Total = "total"  #:
    ByCountry = "byCountry"  #:
    ByInstallation = "byInstallation"  #:
    ByPlayer = "byPlayer"  #:
    ByTankType = "byTankType"  #:
    ByOnshoreOffshoreStatus = "byOnshoreOffshoreStatus"  #:


class InventoriesDronePeriod(Enum):
    """"""

    MidWeeks = "midweeks"  #:
    EiaWeeks = "eia"  #:
    Days = "days"  #:


class DiversionsVesselState(Enum):
    """"""

    Ballast = "Ballast"  #:
    Loaded = "Loaded"  #:


class SupplyDemandSplit(Enum):
    """"""

    Total = "total"  #:
    Country = "country"  #:


class SupplyDemandMetric(Enum):
    """"""

    Supply = "supply"  #:
    Demand = "demand"  #:
    RefineryRun = "refineryRun"  #:
    DirectCrudeUse = "directCrudeUse"  #:
    Balance = "balance"  #:
    NetExport = "netExport"  #:
    StockChange = "stockChange"  #:
    BalancingFactor = "balancingFactor"  #:


class SupplyDemandUsBalancesCrude(Enum):
    """"""

    Adjustment = "adjustment"  #:
    ImportFromCanada = "importFromCanada"  #:
    NetImport = "netImport"  #:
    RefineryRun = "refineryRun"  #:
    Production = "production"  #:
    StockChange = "stockChange"  #:


class SupplyDemandUsBalancesGasoline(Enum):
    """"""

    SupplyByBlender = "supplyByBlender"  #:
    Demand = "demand"  #:
    MaritimeImport = "maritimeImport"  #:
    NetReceipt = "netReceipt"  #:
    StockLevelPadd1A = "stockLevelPadd1A"  #:
    StockLevelPadd1B = "stockLevelPadd1B"  #:
    StockLevelPadd1C = "stockLevelPadd1C"  #:
    PipelineInbound = "pipelineInbound"  #:
    PipelineOutbound = "pipelineOutbound"  #:
    SupplyByRefinery = "supplyByRefinery"  #:
    WaterborneInbound = "waterborneInbound"  #:


class SupplyDemandUsBalancesGranularity(Enum):
    """"""

    Weekly = "weeks"  #:
    Monthly = "months"  #:


class SupplyDemandUsBalancesProduct(Enum):
    """"""

    Crude = "Crude/Co"  #:
    Gasoline = "Gasoline"  #:


class UtilizationGranularity(Enum):
    """"""

    Daily = "day"  #:
    Weekly = "week"  #:
    EiaWeekly = "eia-week"  #:
    Monthly = "month"  #:
    Annually = "year"  #:


class UtilizationSplit(Enum):
    """"""

    Total = "Total"  #:
    RefineryType = "Refinery Type"  #:
    Refinery = "Refinery"  #:
    Country = "Country"  #:
    Subcontinent = "Subcontinent"  #:
    Continent = "Continent"  #:
    TradingRegion = "Trading Region"  #:


class SecondaryFeedGranularity(Enum):
    """"""

    Daily = "day"  #:
    Weekly = "week"  #:
    EiaWeekly = "eia-week"  #:
    Monthly = "month"  #:
    Annually = "year"  #:


class SecondaryFeedSplit(Enum):
    """"""

    Total = "Total"  #:
    RefineryType = "Refinery Type"  #:
    Refinery = "Refinery"  #:
    Country = "Country"  #:
    Subcontinent = "Subcontinent"  #:
    Continent = "Continent"  #:
    TradingRegion = "Trading Region"  #:


class SecondaryFeedUnit(Enum):
    """"""

    KBD = "kbd"  #:
    KB = "kb"  #:
    M3 = "m3"  #:
    MBBL = "Mbbl"  #:


class MarginsGranularity(Enum):
    """"""

    Daily = "day"  #:
    Weekly = "week"  #:
    EiaWeekly = "eia-week"  #:
    Monthly = "month"  #:
    Annually = "year"  #:


class MarginsSplit(Enum):
    """"""

    Total = "Total"  #:
    RefineryType = "Refinery Type"  #:
    Refinery = "Refinery"  #:
    Country = "Country"  #:
    Subcontinent = "Subcontinent"  #:
    Continent = "Continent"  #:
    TradingRegion = "Trading Region"  #:


class FixturesStatuses(Enum):
    """"""

    OnSubs = "on subs"  #:
    InProgress = "in progress"  #:
    FullyFixed = "fully fixed"  #:
    Finished = "finished"  #:
    Failed = "failed"  #:
    Cancelled = "cancelled"  #:


class RefinedProductsGranularity(Enum):
    """"""

    Daily = "day"  #:
    Weekly = "week"  #:
    EiaWeekly = "eia-week"  #:
    Monthly = "month"  #:
    Annually = "year"  #:


class RefinedProducts(Enum):
    """"""

    All = "All"  #:
    TopOfTheBarrel = "Top of the Barrel"  #:
    LPG = "LPG"  #:
    Olefins = "Olefins"  #:
    Naphtha = "Naphtha"  #:
    Gasoline = "Gasoline"  #:
    MiddleOfTheBarrel = "Middle of the Barrel"  #:
    Jet = "Jet"  #:
    LowSulfurDiesel = "Low Sulfur Diesel"  #:
    HighSulfurDiesel = "High Sulfur Diesel"  #:
    BottomOfTheBarrel = "Bottom of the Barrel"  #:
    VGO = "VGO"  #:
    LowSulfurFuelOil = "Low Sulfur Fuel Oil"  #:
    HighSulfurFuelOil = "High Sulfur Fuel Oil"  #:
    Slurry = "Slurry"  #:
    AsphaltBitumen = "Asphalt/Bitumen"  #:
    LubeOils = "LubeOils"  #:
    Petcoke = "Petcoke"  #:


class RefinedProductsSplit(Enum):
    """"""

    Total = "Total"  #:
    RefineryType = "Refinery Type"  #:
    Refinery = "Refinery"  #:
    Country = "Country"  #:
    Subcontinent = "Subcontinent"  #:
    Continent = "Continent"  #:
    TradingRegion = "Trading Region"  #:
    Product = "Product"  #:


class RefinedProductsUnit(Enum):
    """"""

    KBD = "kbd"  #:
    KB = "kb"  #:
    M3 = "m3"  #:
    MBBL = "Mbbl"  #:
    KT = "kt"  #:
    PERCENTAGE = "percentage"  #:
    MT = "Mt"  #:


class RunsGranularity(Enum):
    """"""

    Daily = "day"  #:
    Weekly = "week"  #:
    EiaWeekly = "eia-week"  #:
    Monthly = "month"  #:
    Annually = "year"  #:


class RunsQualities(Enum):
    """"""

    All = "All"  #:
    Light = "Light"  #:
    LightSour = "Light Sour"  #:
    LightSweet = "Light Sweet"  #:
    Medium = "Medium"  #:
    MediumSour = "Medium Sour"  #:
    MediumSweet = "Medium Sweet"  #:
    Heavy = "Heavy"  #:
    HeavySour = "Heavy Sour"  #:
    HeavySweet = "Heavy Sweet"  #:
    Sweet = "Sweet"  #:
    Sour = "Sour"  #:


class RunsSplit(Enum):
    """"""

    Total = "Total"  #:
    RefineryType = "Refinery Type"  #:
    Refinery = "Refinery"  #:
    Country = "Country"  #:
    Subcontinent = "Subcontinent"  #:
    Continent = "Continent"  #:
    TradingRegion = "Trading Region"  #:
    CrudeQuality = "Crude Quality"  #:
    CrudeProductionRegion = "Crude Production Region"  #:


class ImportsSplit(Enum):
    """"""

    Total = "Total"  #:
    RefineryType = "Refinery Type"  #:
    Refinery = "Refinery"  #:
    Country = "Country"  #:
    Subcontinent = "Subcontinent"  #:
    Continent = "Continent"  #:
    TradingRegion = "Trading Region"  #:
    CrudeQuality = "Crude Quality"  #:

    CrudeProductionRegion = "Crude Production Region"  #:


class ImportsMetric(Enum):
    """"""

    Quantity = "Quantity"  #:
    APISulfur = "API Sulfur"  #:


class ImportsGranularity(Enum):
    """"""

    Daily = "day"  #:
    Weekly = "week"  #:
    EiaWeekly = "eia-week"  #:
    Monthly = "month"  #:
    Annually = "year"  #:


class RunsUnit(Enum):
    """"""

    KBD = "kbd"  #:
    KB = "kb"  #:
    M3 = "m3"  #:
    MBBL = "Mbbl"  #:


class ImportsUnit(Enum):
    """"""

    KBD = "kbd"  #:
    KB = "kb"  #:
    M3 = "m3"  #:
    MBBL = "Mbbl"  #:

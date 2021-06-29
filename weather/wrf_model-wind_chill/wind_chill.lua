function dynamic_dataset()
    -- Input datasets
    local t2m  = lib.getData("T2")
    local psfc = lib.getData("PSFC")
    local q2m  = lib.getData("Q2")
    local u10m = lib.getData("U10")
    local v10m = lib.getData("V10")
    -- Output datasets
    local wind_speed = lib.getData("wind_speed")
    local wind_chill = lib.getData("wind_chill")
    local heat_index = lib.getData("heat_index")
    -- Auxiliar variables
    local nx, ny, time = 99, 99, 1
    local CELKEL       = 273.15
    local Rv           = 461.5
    local e_const      = 611
    local epsln        = 0.622
    local L            = 2.5e6
    for i = 1, nx*ny*time do
        wind_speed[i] = math.sqrt(math.pow(u10m[i], 2) + math.pow(v10m[i], 2))
        -- 10-meter wind speed in mph
        local wind_speed_mph = wind_speed[i] * 2.23694
        ---- 2-m temperature in F
        local T2F = (t2m[i]-CELKEL)*(9/5) + 32
        -- Wind Chill in F
        if ((T2F <= 50) and (wind_speed_mph >= 3)) then
            wind_chill[i] = 35.74 + (0.6215 * T2F) - (35.75 * math.pow(wind_speed_mph, 0.16)) + (0.4275 * T2F * math.pow(wind_speed_mph, 0.16))
        else
            wind_chill[i] = T2F
        end
        -- Heat Index in F: first compute 2-m vapor pressure, 2-m saturation vapor pressure, and 2-m RH
        local e2m = q2m[i] * psfc[i] / (epsln + q2m[i])
        local es2m = e_const * math.exp((L/Rv) * ((1/CELKEL) - (1/t2m[i])))
        local rh2m = (e2m/es2m) * 100
        if (rh2m > 100) then
            rh2m = 100
        end
        if ((T2F >= 80) and (rh2m >= 40)) then
            heat_index[i] = -42.379 + (2.04901523 * T2F) + (10.14333127 * rh2m)
            - (0.22475541 * T2F * rh2m) - (6.83783 * 1.e-3 * (math.pow(T2F, 2)))
            - (5.481717 * 1.e-2 * (math.pow(rh2m, 2))) + (1.22874 * 1.e-3 * (math.pow(T2F, 2)) * rh2m)
            + (8.5282 * 1.e-4 * T2F * (math.pow(rh2m, 2))) - (1.99 * 1.e-6 * (math.pow(T2F, 2)) * math.pow(rh2m, 2))
        else
            heat_index[i] = T2F
        end
    end
end

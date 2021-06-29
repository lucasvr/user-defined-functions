function dynamic_dataset()
    local rainc = lib.getData("RAINC")
    local rainnc = lib.getData("RAINNC")
    local rain = lib.getData("RAIN")
    local n = lib.getSize("RAIN")[1]

    for i=1, n do
        rain[i] = (rainc[i] + rainnc[i])
    end
end

export interface SaveEcoBotMeteoValue {
    value: number | string;
    updated_at: string;
    is_old: boolean;
}

export interface SaveEcoBotCity {
    id: number;
    city_name: string;
    aqi: number;
    aqi_is_old: boolean;
    aqi_updated_at: string;
    center_latitude: string;
    center_longitude: string;
    link_maps_aqi: string;
    link_maps_gamma: string;
    link: string;
    meteo: {
        wind_power: SaveEcoBotMeteoValue;
        wind_direction: SaveEcoBotMeteoValue;
        temperature: SaveEcoBotMeteoValue;
        humidity: SaveEcoBotMeteoValue;
        pressure_pa: SaveEcoBotMeteoValue;
    };
}

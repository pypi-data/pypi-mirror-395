export interface hajimiParams {
    id: number
    hajimi_name: string
    hajimi_age: number
    hajimi_breed: string
    hajimi_color: string
    hajimi_gender: string
    hajimi_weight: number
    hajimi_height: number
    hajimi_health: string
    hajimi_vaccination: string
    hajimi_vaccination_date: string
    hajimi_vaccination_place: string
}

export interface hajimiResponse {
    code: number
    message: string
    data: hajimiParams
}
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class StoreStationRequest extends FormRequest
{
    /**
     * Determine if the user is authorized to make this request.
     */
    public function authorize(): bool
    {
        return true;
    }

    /**
     * Get the validation rules that apply to the request.
     *
     * @return array<string, \Illuminate\Contracts\Validation\ValidationRule|array|string>
     */
    public function rules(): array
    {
        return [
            'code'            => 'required|alpha_num',
            'name'            => 'required|string',
            'description'     => 'nullable|string',
            'latitude'        => 'required|numeric|between:-90,90',
            'longitude'       => 'required|numeric|between:-180,180',
            'heigth'          => 'required|numeric|min:0',
            'automatica'      => 'required|boolean',
            'id_institute'    => 'required|integer',
            'id_type_station' => 'required|integer',
            'id_county'       => 'required|integer'
        ];
    }    
}

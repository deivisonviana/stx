<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Http\Exceptions\HttpResponseException;
use Illuminate\Contracts\Validation\Validator;

class StoreRecordRequest extends FormRequest
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
            'records'               => 'required|array',
            'records.*'             => 'required|array',
            'records.*.date_hour'   => 'required|date',
            'records.*.instant'     => 'required|numeric',
            'records.*.maximun'     => 'nullable|numeric',
            'records.*.minimun'     => 'nullable|numeric',
            'records.*.average'     => 'nullable|numeric',
            'records.*.id_station'  => 'required|integer',
            'records.*.id_variable' => 'required|integer',
            'records.*.id_flag'     => 'required|integer',
        ];
    }

    /**
     * Undocumented function
     *
     * @param \Illuminate\Contracts\Validation\Validator $validator
     * 
     * @return void
     */
    protected function failedValidation(Validator $validator): void
    {
        throw new HttpResponseException(
            response()->json([
                'success' => false,
                'message' => 'Erro de validacao',
                'errors' => $validator->errors(),
            ], 422)
        );
    }
}

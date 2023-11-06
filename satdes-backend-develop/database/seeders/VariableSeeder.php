<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

class VariableSeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {   
        // Lista com as possiveis variaveis do banco
        $variables = [
            ['name' => 'Temperatura Interna',      'code' => 'TEMP_INT', 'id_type_unit' => 1],
            ['name' => 'Temperatura ',             'code' => 'TEMP',     'id_type_unit' => 1],
            ['name' => 'Temperatura NTC',          'code' => 'TEMP_NTC', 'id_type_unit' => 1],
            ['name' => 'Temperatura do Solo',      'code' => 'TEMP_SLO', 'id_type_unit' => 1],
            ['name' => 'Umidade Relativa',         'code' => 'UMID_REL', 'id_type_unit' => 3],
            ['name' => 'Umidade do Solo',          'code' => 'UMID_SLO', 'id_type_unit' => 3],
            ['name' => 'Presão Atmosferica',       'code' => 'PRES_ATM', 'id_type_unit' => 2],
            ['name' => 'Radiação Solar Global',    'code' => 'RADS_GLB', 'id_type_unit' => 4],
            ['name' => 'Radiação Solar Liquida',   'code' => 'RADS_LIQ', 'id_type_unit' => 4],
            ['name' => 'Radiação Solar Refletida', 'code' => 'RADS_REF', 'id_type_unit' => 4],
            ['name' => 'Radiação Solar IV',        'code' => 'RADS_IV',  'id_type_unit' => 4],
            ['name' => 'Radiação Solar SPF',       'code' => 'RADS_SPF', 'id_type_unit' => 4],
            ['name' => 'Direção do Vento',         'code' => 'DIR_VEN',  'id_type_unit' => 5],
            ['name' => 'Velocidade do Vento',      'code' => 'VEL_VEN',  'id_type_unit' => 6],
            ['name' => 'Precipitação',             'code' => 'PREC',     'id_type_unit' => 7],
            ['name' => 'Ponto de Orvalho',         'code' => 'PONT_ORV', 'id_type_unit' => 1],
            ['name' => 'Rajada de Vento',          'code' => 'RAJ_VEN',  'id_type_unit' => 6],
            ['name' => 'Nebulosidade',             'code' => 'NEBU',     'id_type_unit' => 11],
            ['name' => 'Insolação Solar',          'code' => 'INSO_SOL', 'id_type_unit' => 11],
        ];

        DB::table('variables')->insert($variables);
    }
}

<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

class ConfigStationSeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        // Carrega o mapeamento de variaveis do modelo atual de estações do INMET
        $loadJSon = function($name) {
            return json_decode(file_get_contents(__DIR__."/../../database/{$name}.json"));
        };

        $config = [
            [
                'model_code' => 'INMET',
                'config'     => json_encode($loadJSon('inmet_map'))
            ],
            [
                'model_code' => 'CEPDEC',
                'config'     => json_encode($loadJSon('cepdec_map'))
            ],
        ];

        DB::table('config_stations')->insert($config);
    }
}

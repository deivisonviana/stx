<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

class TypeStationSeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        $types = [
            ['type' => 'Meteorologica'],
            ['type' => 'Agro-Meteorologica'],
            ['type' => 'Pluviometrica'],
            ['tyoe' => 'Fluviometro'],
            ['type' => 'Pesquisa']
        ];

        DB::table('type_stations')->insert($types);
    }
}

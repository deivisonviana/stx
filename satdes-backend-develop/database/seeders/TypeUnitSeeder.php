<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

class TypeUnitSeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        $measures = [
            ['acronym' => 'ºC',   'measure' => 'Graus Celsius'],              // 1
            ['acronym' => 'hPa',  'measure' => 'Hectopascal'],                // 2
            ['acronym' => '%',    'measure' => 'Por cento'],                  // 3
            ['acronym' => 'W/m²', 'measure' => 'Watts por metro quadrado'],   // 4
            ['acronym' => 'º',    'measure' => 'Graus'],                      // 5
            ['acronym' => 'm/s',  'measure' => 'Metros por segundo'],         // 6
            ['acronym' => 'mm',   'measure' => 'Milímetro'],                  // 7
            ['acronym' => 'cm',   'measure' => 'Centímetro'],                 // 8
            ['acronym' => 'V',    'measure' => 'Volts'],                      // 9
            ['acronym' => 'm³/s', 'measure' => 'Metros cúbicos por segundo'], // 10
            ['acronym' => 'N',    'measure' => 'Decimal']                     // 11
        ];
         
        DB::table('type_units')->insert($measures);
    }
}

<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

class FlagSeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        $flags = [
            ['quality' => 'dado aprovado'],
            ['quality' => 'dado suspeito'],
            ['quality' => 'dado com possível erro'],
            ['quality' => 'dado reprovado'],
            ['quality' => 'dado não verificado'],
            ['quality' => 'não há instrumento instalado no local'],
            ['quality' => 'falta registro de dados']
        ];
        
        DB::table('flags')->insert($flags);
    }
}

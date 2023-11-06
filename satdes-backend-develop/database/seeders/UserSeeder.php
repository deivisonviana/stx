<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

class UserSeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        $users = [
            [
                'name' => 'INCAPER',
                'email' => 'incaper@es.gov.br',
                'password' => 'password'
            ],
            [
                'name' => 'CEPDEC',
                'email' => 'cepdec@es.gov.br',
                'password' => 'password'
            ],
            [
                'name' => 'INMET',
                'email' => 'inmet@gov.br',
                'password' => 'password'
            ],
            [
                'name' => 'ANA',
                'email' => 'ana@gov.br',
                'password' => 'password'
            ],
        ];

        DB::table('users')->insert($users);
    }
}
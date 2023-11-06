<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

class CountySeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        $counties = [
            ['name' => 'Afonso Cláudio', 'id_state' => 8],
            ['name' => 'Água Doce do Norte', 'id_state' => 8],
            ['name' => 'Águia Branca', 'id_state' => 8],
            ['name' => 'Alegre', 'id_state' => 8],
            ['name' => 'Alfredo Chaves', 'id_state' => 8],
            ['name' => 'Alto Rio Novo', 'id_state' => 8],
            ['name' => 'Anchieta', 'id_state' => 8],
            ['name' => 'Apiacá', 'id_state' => 8],
            ['name' => 'Aracruz', 'id_state' => 8],
            ['name' => 'Atilio Vivacqua', 'id_state' => 8],
            ['name' => 'Baixo Guandu', 'id_state' => 8],
            ['name' => 'Barra de São Francisco', 'id_state' => 8],
            ['name' => 'Boa Esperança', 'id_state' => 8],
            ['name' => 'Bom Jesus do Norte', 'id_state' => 8],
            ['name' => 'Brejetuba', 'id_state' => 8],
            ['name' => 'Cachoeiro de Itapemirim', 'id_state' => 8],
            ['name' => 'Cariacica', 'id_state' => 8],
            ['name' => 'Castelo', 'id_state' => 8],
            ['name' => 'Colatina', 'id_state' => 8],
            ['name' => 'Conceição da Barra', 'id_state' => 8],
            ['name' => 'Conceição do Castelo', 'id_state' => 8],
            ['name' => 'Divino de São Lourenço', 'id_state' => 8],
            ['name' => 'Domingos Martins', 'id_state' => 8],
            ['name' => 'Dores do Rio Preto', 'id_state' => 8],
            ['name' => 'Ecoporanga', 'id_state' => 8],
            ['name' => 'Fundão', 'id_state' => 8],
            ['name' => 'Governador Lindenberg', 'id_state' => 8],
            ['name' => 'Guaçuí', 'id_state' => 8],
            ['name' => 'Guarapari', 'id_state' => 8],
            ['name' => 'Ibatiba', 'id_state' => 8],
            ['name' => 'Ibiraçu', 'id_state' => 8],
            ['name' => 'Ibitirama', 'id_state' => 8],
            ['name' => 'Iconha', 'id_state' => 8],
            ['name' => 'Irupi', 'id_state' => 8],
            ['name' => 'Itaguaçu', 'id_state' => 8],
            ['name' => 'Itapemirim', 'id_state' => 8],
            ['name' => 'Itarana', 'id_state' => 8],
            ['name' => 'Iúna', 'id_state' => 8],
            ['name' => 'Jaguaré', 'id_state' => 8],
            ['name' => 'Jerônimo Monteiro', 'id_state' => 8],
            ['name' => 'João Neiva', 'id_state' => 8],
            ['name' => 'Laranja da Terra', 'id_state' => 8],
            ['name' => 'Linhares', 'id_state' => 8],
            ['name' => 'Mantenópolis', 'id_state' => 8],
            ['name' => 'Marataízes', 'id_state' => 8],
            ['name' => 'Marechal Floriano', 'id_state' => 8],
            ['name' => 'Marilândia', 'id_state' => 8],
            ['name' => 'Mimoso do Sul', 'id_state' => 8],
            ['name' => 'Montanha', 'id_state' => 8],
            ['name' => 'Mucurici', 'id_state' => 8],
            ['name' => 'Muniz Freire', 'id_state' => 8],
            ['name' => 'Muqui', 'id_state' => 8],
            ['name' => 'Nova Venécia', 'id_state' => 8],
            ['name' => 'Pancas', 'id_state' => 8],
            ['name' => 'Pedro Canário', 'id_state' => 8],
            ['name' => 'Pinheiros', 'id_state' => 8],
            ['name' => 'Piúma', 'id_state' => 8],
            ['name' => 'Ponto Belo', 'id_state' => 8],
            ['name' => 'Presidente Kennedy', 'id_state' => 8],
            ['name' => 'Rio Bananal', 'id_state' => 8],
            ['name' => 'Rio Novo do Sul', 'id_state' => 8],
            ['name' => 'Santa Leopoldina', 'id_state' => 8],
            ['name' => 'Santa Maria de Jetibá', 'id_state' => 8],
            ['name' => 'Santa Teresa', 'id_state' => 8],
            ['name' => 'São Domingos do Norte', 'id_state' => 8],
            ['name' => 'São Gabriel da Palha', 'id_state' => 8],
            ['name' => 'São José do Calçado', 'id_state' => 8],
            ['name' => 'São Mateus', 'id_state' => 8],
            ['name' => 'São Roque do Canaã', 'id_state' => 8],
            ['name' => 'Serra', 'id_state' => 8],
            ['name' => 'Sooretama', 'id_state' => 8],
            ['name' => 'Vargem Alta', 'id_state' => 8],
            ['name' => 'Venda Nova do Imigrante', 'id_state' => 8],
            ['name' => 'Viana', 'id_state' => 8],
            ['name' => 'Vila Pavão', 'id_state' => 8],
            ['name' => 'Vila Valério', 'id_state' => 8],
            ['name' => 'Vila Velha', 'id_state' => 8],
            ['name' => 'Vitória', 'id_state' => 8],
        ];

        DB::table('counties')->insert($counties);
    }
}
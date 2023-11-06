<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Http\Requests\StoreStationRequest;
use App\Http\Requests\UpdateStationRequest;
use Illuminate\Http\Request;
use App\Models\Station;
use Spatie\QueryBuilder\AllowedFilter;
use Spatie\QueryBuilder\QueryBuilder;

class StationController extends Controller
{   
    /**
     * Display a listing of the resource.
     */
    public function index(Request $request)
    {   
        $queryBuilder = QueryBuilder::for(Station::class)
            ->allowedFilters([
                AllowedFilter::exact('institute', 'id_institute'),
                AllowedFilter::exact('automatic')->ignore([0, 1]),
                AllowedFilter::exact('type', 'id_type_station')
            ]);
        $stations = Station::completeInfo($queryBuilder);

        // Retorne os resultados da consulta.
        return $this->successResponse('Estações consultadas com sucesso!', 200, $stations);
    }

    /**
     * Store a newly created resource in storage.
     */
    public function store(StoreStationRequest $request)
    {
        // Valida os dados da solicitação usando a classe StoreStationRequest.
        $validated = $request->validated();

        try {
            // Cria uma nova instância de Station com os dados validados.
            Station::create($validated);

            // Retorna uma resposta de sucesso com código 201 (Recurso criado com sucesso).
            return $this->successResponse('Estação cadastrada com sucesso!', 201);

        } catch (\Illuminate\Database\QueryException $e) {
            // Retorna uma resposta de erro com detalhes da exceção em caso de falha.
            return $this->errorResponse('Erro ao criar estação', 500, $e->getMessage());
        }
    }

    /**
     * Display the specified resource.
     */
    public function show(string $id)
    {
        // Procura uma estação com o ID especificado.
        $station = Station::find($id);

        // Verifica se a estação foi encontrada.
        if (!$station) {
            return $this->errorResponse('Estação não encontrada!', 400);
        }
        // Retorna uma resposta de sucesso com os detalhes da estação.
        return $this->successResponse('Estação encontrada com sucesso!', 200, $station);
    }

     /**
     * Update the specified resource in storage.
     */
    public function update(UpdateStationRequest $request, string $id)
    {
        // Procura uma estação com o ID especificado.
        $station = Station::find($id);

        // Verifica se a estação foi encontrada.
        if (!$station) {
            return $this->errorResponse('Estação não encontrada!', 404);
        }
        // Valida os dados recebidos no request usando a classe UpdateStationRequest.
        $validated = $request->validated();
        
        try {
            // Atualiza os dados da estação com base nos dados validados.
            $station->update($validated);

            // Retorna uma resposta de sucesso com código 200.
            return $this->successResponse('Estação atualizada com sucesso!', 200);

        } catch (\Exception $e) {
            // Retorna uma resposta de erro com detalhes da exceção em caso de falha.
            return $this->errorResponse('Erro ao atualizar estação', 500, $e->getMessage());
        }
    }

    /**
     * Remove the specified resource from storage.
     */
    public function destroy(string $id)
    {
        // Procura uma estação com o ID especificado.
        $station = Station::find($id);

        // Verifica se a estação foi encontrada.
        if (!$station) {
            return $this->errorResponse('Estação não encontrada!', 404);
        }

        try {
            // Exclui a estação do armazenamento.
            $station->delete();

            // Retorna uma resposta de sucesso com código 200.
            return $this->successResponse('Estação excluída com sucesso!', 200);

        } catch (\Exception $e) {
            // Retorna uma resposta de erro com detalhes da exceção em caso de falha.
            return $this->errorResponse('Erro ao excluir estação', 500, $e->getMessage());
        }
    }
}

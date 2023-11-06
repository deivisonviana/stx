<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Http\Requests\QueryRecordRequest;
use App\Http\Requests\StoreRecordRequest;
use App\Http\Resources\RecordResource;
use App\Models\Record;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Validator;
use Spatie\QueryBuilder\AllowedFilter;
use Spatie\QueryBuilder\QueryBuilder;

class RecordController extends Controller
{
    /**
     * Display a listing of the resource.
     */
    public function index()
    {   
        $queryBuilder = QueryBuilder::for(Record::class)
            ->allowedFilters([
                AllowedFilter::exact('code', 'id_station'),
            ])->get();

        return $this->successResponse('Registros méteorologicos consultados', 200, $queryBuilder);
    }

    /**
     * Store a newly created resource in storage.
     */
    public function store(StoreRecordRequest $request)
    {
        // Valida os dados da solicitação usando a classe StoreStationRequest.
        $validated = $request->validated();

        // Suponha que $validated['records'] seja uma matriz
        $records = collect($validated['records']);

        $filteredRecords = $records->filter(function ($record) {
            return isset($record['instant']);
        });

        // Verifique se há registros válidos após a filtragem
        if ($filteredRecords->isEmpty()) {
            return $this->errorResponse('Nenhum registro válido encontrado para cadastro!', 400);
        }
        
        try {
            Record::insert($filteredRecords);

            return $this->successResponse('Dados cadastrados com sucesso!', 201); 

        } catch(\Illuminate\Database\QueryException $e) {

            return $this->errorResponse('Erro ao cadastrar dados', 500, $e->getMessage());
        } 
    }

    /**
     * Display the specified resource.
     */
    public function show(string $id)
    {
        
    }

    /**
     * Update the specified resource in storage.
     */
    public function update(Request $request, string $id)
    {
        
    }

    /**
     * Remove the specified resource from storage.
     */
    public function destroy(string $id)
    {
        
    }

    /**
     * Consulta registros com base no código, data de inicio e data de termino.
     *
     * @param \App\Http\Requests\QueryRecordRequest $request
     * @param string $code
     * @param string $start
     * @param string $end
     * @return 
     */
    public function selectRecords(QueryRecordRequest $request, $code, $start, $end)
    {
        $records = Record::getBruteData($code, [
            'start' => $start,
            'end'   => $end
        ]);
        // Verifica se a consulta obteve resultado
        if ($records->isEmpty()) {
            return $this->errorResponse('Não foram encontrados registros nessa data!', 400, $records);

        } else {
            return $this->successResponse('Dados consultados', 200, $records);        
        }
    }

    /**
     * Consulta registros especificos para gerar os graficos, com base no código data de inicio e data de termino.
     *
     * @param string $code
     * @param string $start
     * @param string $end
     * 
     * @return \Illuminate\Http\Response
     */
    public function selectProducts(QueryRecordRequest $request, $code, $start, $end)
    {
        $records = Record::getGraphicsData($code, [
            'start' => $start,
            'end'   => $end
        ]);
        // Verifica se a consulta obteve resultado
        if ($records->isEmpty()) {
            return $this->errorResponse('Não foram encontrados registros nessa data!.', 400, $records);

        } else {
            return $this->successResponse('Requisição bem sussedida', 200, $records);
        }
    }
}

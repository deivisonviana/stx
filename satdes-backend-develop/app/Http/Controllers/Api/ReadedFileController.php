<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\ReadedFile;
use Illuminate\Http\Request;
use Spatie\QueryBuilder\AllowedFilter;
use Spatie\QueryBuilder\QueryBuilder;

class ReadedFileController extends Controller
{
    /**
     * Display a listing of the resource.
     */
    public function index()
    {
        $queryBuilder = QueryBuilder::for(ReadedFile::class)
            ->allowedFilters([
                AllowedFilter::exact('station', 'id_station'),
                'stations.name'
            ]);
            
        $stationFiles = ReadedFile::registeredData($queryBuilder);

        if ($stationFiles->isEmpty()) {
            return $this->successResponse('Não existe arquivos lidos!', 200);
        } 
        return $this->successResponse('Dados lidos com sucesso!', 200, $stationFiles);
    }

    /**
     * Store a newly created resource in storage.
     */
    public function store(Request $request)
    {
        //
    }

    /**
     * Display the specified resource.
     */
    public function show(string $id)
    {
        //
    }

    /**
     * Update the specified resource in storage.
     */
    public function update(Request $request, string $id)
    {
        //
    }

    /**
     * Remove the specified resource from storage.
     */
    public function destroy(string $id)
    {
        //
    }
}

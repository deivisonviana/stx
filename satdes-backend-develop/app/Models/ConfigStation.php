<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class ConfigStation extends Model
{
    use HasFactory;

    /**
     * The table associated with the model.
     *
     * @var string
     */
    protected $table = 'config_stations';

    /**
     * The attributes that are mass assignable.
     *
     * @var array<int, string>
     */
    protected $fillable = [
        'model_code',
        'config'
    ];

    /**
     * Consulta os dados das estações, configurações filtrado pela instituição
     * @param \Spatie\QueryBuilder\QueryBuilder $query
     * 
     * @return 
     */
    public static function MappedData($query) 
    {
        return $query->select(
            'stations.id', 
            'stations.name',
            'stations.code', 
            'config_stations.config'
            )
            ->join('config_stations', 'stations.id_config_station', '=', 'config_stations.id')
            ->join('institutes', 'stations.id_institute', '=', 'institutes.id')
            ->whereNotNull('config_stations.config')
            ->get();
    }
}

<?php

namespace App\Models;

use App\Models\Institute;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Station extends Model
{
    use HasFactory;

    /**
     * The table associated with the model.
     *
     * @var string
     */
    protected $table = 'stations';

    /**
     * The attributes that are mass assignable.
     *
     * @var array<int, string>
     */
    protected $fillable = [
        'code',
        'name',
        'description',
        'latitude',
        'longitude',
        'height',
        'automatic',
        'operation_begin',
        'operation_ended',
        'patrimony',
        'id_config_station',
        'id_institute',
        'id_type_station',
        'id_county'
    ];

    /**
     * Get the institute that owns the station 
     */
    public function institute(): BelongsTo
    {
        return $this->belongsTo(Institute::class, 'id_institute');
    }

    /**
     * Get the type of the station belongs 
     */
    public function type(): BelongsTo
    {
        return $this->belongsTo(TypeStation::class, 'id_type_station');
    }

    /**
     * Get the county that owns the station
     */
    public function county(): BelongsTo
    {
        return $this->belongsTo(County::class, 'id_county');
    }

    /**
     * Get the config variables of the station
     */
    public function config(): BelongsTo
    {
        return $this->belongsTo(ConfigStation::class, 'id_config_station');
    }

    /**
     * Undocumented function
     *
     * @param \Spatie\QueryBuilder\QueryBuilder $query
     * @return 
     */
    public static function completeInfo($query) {
        return $query->select(
            'stations.id',
            'stations.code',
            'stations.name',
            'stations.description',
            'stations.latitude',
            'stations.longitude',
            'stations.height',
            'stations.automatic',
            'stations.operation_begin',
            'stations.operation_ended',
            'stations.id_institute',
            'users.name as name_institute',
            'type_stations.type'
        )
        ->join('type_stations', 'stations.id_type_station', '=', 'type_stations.id')
        ->join('institutes', 'stations.id_institute', '=', 'institutes.id')
        ->join('users', 'institutes.id_user', '=', 'users.id')
        ->get();
    }
}

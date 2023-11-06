<?php

namespace App\Http\Middleware;

use DateTime;
use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class DateRangeValidator
{
    /**
     * Handle an incoming request.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next): Response
    {
        // Obtendo os parametros da requisição
        $dateStart = $request->route('start');
        $dateEnd   = $request->route('end');
        
        // Verifica se ambos os parametros estão definidos
        if ($dateStart and $dateEnd) {
            // Instancias de objetos
            $dateStart = new DateTime($dateStart);
            $dateEnd   = new DateTime($dateEnd);
        
            // Calcule a diferença entre as datas
            $interval = $dateStart->diff($dateEnd);

            // Verifique se a diferença é menor ou igual a 6 meses
            if ($interval->y * 12 + $interval->m > 6) {
                return response()->json([
                    'success' => false,
                    'message' => 'Erro, a diferença entre as datas excede 6 meses.',
                    'data'    => null,
                ], 400);
            }
        }
        return $next($request);
    }
}

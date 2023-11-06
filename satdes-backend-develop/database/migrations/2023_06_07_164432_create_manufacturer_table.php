<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('manufacters', function (Blueprint $table) {
            // Columns
            $table->id();
            $table->string('name', 25);

            // Comment
            $table->comment('Tabela com os dados referentes ao fabricante do sensor');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('manufacters');
    }
};

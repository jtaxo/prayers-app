// CONFIGURAÇÃO DO SUPABASE
// Substitua os valores abaixo com as credenciais obtidas no painel do Supabase (Settings -> API)
const SUPABASE_URL = "https://ujfbjtstkiaeldqxbdvp.supabase.co";
const SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVqZmJqdHN0a2lhZWxkcXhiZHZwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODQxOTc2NzQsImV4cCI6MjA5OTc3MzY3NH0.mo-fEUUOatYTzFnscvGr3Ph9hc1XcLMtYJkM4cpFFXs";

// Inicialização do cliente
const supabaseClient = supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

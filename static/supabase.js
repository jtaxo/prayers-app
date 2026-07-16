// CONFIGURAÇÃO DO SUPABASE
// Substitua os valores abaixo com as credenciais obtidas no painel do Supabase (Settings -> API)
const SUPABASE_URL = "https://SEU_PROJETO.supabase.co";
const SUPABASE_ANON_KEY = "SUA_CHAVE_ANON_PUBLICA";

// Inicialização do cliente
const supabaseClient = supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

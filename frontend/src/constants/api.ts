export const API_ROUTES = {
  AUTH: {
    LOGIN: '/auth/login',
    REGISTER: '/auth/register',
    REFRESH: '/auth/refresh',
    LOGOUT: '/auth/logout'
  },
  DOCUMENTS: {
    LIST: '/documents',
    CREATE: '/documents',
    GET: (id: number) => `/documents/${id}`,
    UPDATE: (id: number) => `/documents/${id}`,
    DELETE: (id: number) => `/documents/${id}`
  },
  ORG: {
    PARSE: '/org/parse',
    EXPORT: '/org/export'
  }
} 
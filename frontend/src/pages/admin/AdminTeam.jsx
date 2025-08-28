import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Input } from '../../components/ui/input';
import { Badge } from '../../components/ui/badge';
import { Avatar, AvatarFallback, AvatarImage } from '../../components/ui/avatar';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '../../components/ui/dialog';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../../components/ui/select';
import { 
  ArrowLeft,
  Users,
  Plus,
  Edit,
  Trash2,
  Shield,
  Eye,
  EyeOff,
  Search,
  Filter,
  UserPlus,
  Settings,
  CheckCircle,
  XCircle
} from 'lucide-react';
import { toast } from 'sonner';

const AdminTeam = () => {
  const navigate = useNavigate();
  const [teamMembers, setTeamMembers] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [roleFilter, setRoleFilter] = useState('all');
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [editingMember, setEditingMember] = useState(null);
  const [showPassword, setShowPassword] = useState(false);
  const [teamForm, setTeamForm] = useState({
    fullName: '',
    email: '',
    phone: '',
    username: '',
    password: '',
    role: 'agent',
    department: '',
    joiningDate: '',
    isActive: true
  });

  useEffect(() => {
    const token = localStorage.getItem('adminToken');
    if (!token) {
      navigate('/admin/login');
      return;
    }
    fetchTeamMembers();
  }, [navigate]);

  const fetchTeamMembers = async () => {
    try {
      setIsLoading(true);
      // Mock data for now - replace with actual API call
      const mockTeamMembers = [
        {
          id: '1',
          fullName: 'Admin User',
          email: 'admin@gmbtravelskashmir.com',
          phone: '+91 98765 43210',
          username: 'admin',
          role: 'admin',
          department: 'Management',
          joiningDate: '2024-01-01',
          isActive: true,
          lastLogin: '2024-11-27T10:30:00Z',
          packagesCreated: 15,
          clientsManaged: 45,
          avatar: null
        },
        {
          id: '2',
          fullName: 'Rajesh Kumar',
          email: 'rajesh.manager@gmbtravelskashmir.com',
          phone: '+91 87654 32109',
          username: 'rajesh_manager',
          role: 'manager',
          department: 'Operations',
          joiningDate: '2024-02-15',
          isActive: true,
          lastLogin: '2024-11-26T15:45:00Z',
          packagesCreated: 12,
          clientsManaged: 38,
          avatar: null
        },
        {
          id: '3',
          fullName: 'Priya Sharma',
          email: 'priya.agent@gmbtravelskashmir.com',
          phone: '+91 76543 21098',
          username: 'priya_agent',
          role: 'agent',
          department: 'Sales',
          joiningDate: '2024-03-10',
          isActive: true,
          lastLogin: '2024-11-27T09:20:00Z',
          packagesCreated: 8,
          clientsManaged: 28,
          avatar: null
        },
        {
          id: '4',
          fullName: 'Amit Patel',
          email: 'amit.agent@gmbtravelskashmir.com',
          phone: '+91 65432 10987',
          username: 'amit_agent',
          role: 'agent',
          department: 'Customer Support',
          joiningDate: '2024-04-05',
          isActive: false,
          lastLogin: '2024-11-20T14:30:00Z',
          packagesCreated: 5,
          clientsManaged: 15,
          avatar: null
        }
      ];
      setTeamMembers(mockTeamMembers);
    } catch (error) {
      toast.error('Failed to fetch team members');
    } finally {
      setIsLoading(false);
    }
  };

  const handleInputChange = (field, value) => {
    setTeamForm(prev => ({ ...prev, [field]: value }));
  };

  const resetForm = () => {
    setTeamForm({
      fullName: '',
      email: '',
      phone: '',
      username: '',
      password: '',
      role: 'agent',
      department: '',
      joiningDate: '',
      isActive: true
    });
    setEditingMember(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      if (editingMember) {
        // Update team member
        setTeamMembers(prev => 
          prev.map(member => 
            member.id === editingMember.id 
              ? { ...member, ...teamForm, packagesCreated: member.packagesCreated, clientsManaged: member.clientsManaged }
              : member
          )
        );
        toast.success('Team member updated successfully!');
      } else {
        // Create new team member
        const newMember = {
          id: Date.now().toString(),
          ...teamForm,
          lastLogin: null,
          packagesCreated: 0,
          clientsManaged: 0,
          avatar: null
        };
        setTeamMembers(prev => [newMember, ...prev]);
        toast.success('Team member added successfully!');
      }
      
      resetForm();
      setIsDialogOpen(false);
    } catch (error) {
      toast.error('Failed to save team member');
    }
  };

  const handleEdit = (member) => {
    setEditingMember(member);
    setTeamForm({
      fullName: member.fullName,
      email: member.email,
      phone: member.phone,
      username: member.username,
      password: '', // Don't populate password for security
      role: member.role,
      department: member.department,
      joiningDate: member.joiningDate,
      isActive: member.isActive
    });
    setIsDialogOpen(true);
  };

  const handleDelete = async (memberId) => {
    if (window.confirm('Are you sure you want to delete this team member?')) {
      try {
        setTeamMembers(prev => prev.filter(member => member.id !== memberId));
        toast.success('Team member deleted successfully');
      } catch (error) {
        toast.error('Failed to delete team member');
      }
    }
  };

  const toggleMemberStatus = async (memberId) => {
    try {
      setTeamMembers(prev => 
        prev.map(member => 
          member.id === memberId 
            ? { ...member, isActive: !member.isActive }
            : member
        )
      );
      toast.success('Member status updated');
    } catch (error) {
      toast.error('Failed to update member status');
    }
  };

  const filteredMembers = teamMembers.filter(member => {
    const matchesSearch = member.fullName.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         member.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         member.username.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesRole = roleFilter === 'all' || member.role === roleFilter;
    return matchesSearch && matchesRole;
  });

  const getRoleColor = (role) => {
    switch (role) {
      case 'admin': return 'bg-red-100 text-red-700 border-red-200';
      case 'manager': return 'bg-blue-100 text-blue-700 border-blue-200';
      case 'agent': return 'bg-green-100 text-green-700 border-green-200';
      default: return 'bg-slate-100 text-slate-700 border-slate-200';
    }
  };

  const getRoleIcon = (role) => {
    switch (role) {
      case 'admin': return <Shield className="h-4 w-4" />;
      case 'manager': return <Settings className="h-4 w-4" />;
      case 'agent': return <Users className="h-4 w-4" />;
      default: return <Users className="h-4 w-4" />;
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-IN', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Link to="/admin/dashboard">
                <Button variant="ghost" size="sm">
                  <ArrowLeft className="h-4 w-4 mr-2" />
                  Back to Dashboard
                </Button>
              </Link>
              <div className="flex items-center space-x-3">
                <Users className="h-6 w-6 text-amber-600" />
                <div>
                  <h1 className="text-xl font-bold text-slate-800">Team Management</h1>
                  <p className="text-sm text-slate-600">Manage team members and user accounts</p>
                </div>
              </div>
            </div>
            <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
              <DialogTrigger asChild>
                <Button onClick={resetForm} className="bg-amber-600 hover:bg-amber-700">
                  <UserPlus className="h-4 w-4 mr-2" />
                  Add Team Member
                </Button>
              </DialogTrigger>
              <DialogContent className="max-w-2xl">
                <DialogHeader>
                  <DialogTitle>{editingMember ? 'Edit Team Member' : 'Add New Team Member'}</DialogTitle>
                  <DialogDescription>
                    {editingMember ? 'Update team member information' : 'Fill in the details to add a new team member'}
                  </DialogDescription>
                </DialogHeader>
                
                <form onSubmit={handleSubmit} className="space-y-6">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-slate-700 mb-2">Full Name *</label>
                      <Input
                        type="text"
                        value={teamForm.fullName}
                        onChange={(e) => handleInputChange('fullName', e.target.value)}
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-slate-700 mb-2">Email *</label>
                      <Input
                        type="email"
                        value={teamForm.email}
                        onChange={(e) => handleInputChange('email', e.target.value)}
                        required
                      />
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-slate-700 mb-2">Phone Number *</label>
                      <Input
                        type="tel"
                        value={teamForm.phone}
                        onChange={(e) => handleInputChange('phone', e.target.value)}
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-slate-700 mb-2">Department</label>
                      <Input
                        type="text"
                        placeholder="e.g., Sales, Operations, Support"
                        value={teamForm.department}
                        onChange={(e) => handleInputChange('department', e.target.value)}
                      />
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-slate-700 mb-2">Username *</label>
                      <Input
                        type="text"
                        value={teamForm.username}
                        onChange={(e) => handleInputChange('username', e.target.value)}
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-slate-700 mb-2">
                        {editingMember ? 'New Password (leave blank to keep current)' : 'Password *'}
                      </label>
                      <div className="relative">
                        <Input
                          type={showPassword ? "text" : "password"}
                          value={teamForm.password}
                          onChange={(e) => handleInputChange('password', e.target.value)}
                          required={!editingMember}
                        />
                        <button
                          type="button"
                          onClick={() => setShowPassword(!showPassword)}
                          className="absolute right-3 top-3 text-slate-400 hover:text-slate-600"
                        >
                          {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                        </button>
                      </div>
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-slate-700 mb-2">Role *</label>
                      <Select value={teamForm.role} onValueChange={(value) => handleInputChange('role', value)}>
                        <SelectTrigger>
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="admin">Admin (Full Access)</SelectItem>
                          <SelectItem value="manager">Manager (Manage Packages & Reports)</SelectItem>
                          <SelectItem value="agent">Agent/Staff (Handle Clients)</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-slate-700 mb-2">Joining Date</label>
                      <Input
                        type="date"
                        value={teamForm.joiningDate}
                        onChange={(e) => handleInputChange('joiningDate', e.target.value)}
                      />
                    </div>
                  </div>

                  <div className="flex items-center space-x-2">
                    <input
                      type="checkbox"
                      id="isActive"
                      checked={teamForm.isActive}
                      onChange={(e) => handleInputChange('isActive', e.target.checked)}
                      className="rounded border-slate-300"
                    />
                    <label htmlFor="isActive" className="text-sm text-slate-700">
                      Active (user can login and access system)
                    </label>
                  </div>

                  <div className="flex justify-end space-x-4 pt-4 border-t">
                    <Button type="button" variant="outline" onClick={() => setIsDialogOpen(false)}>
                      Cancel
                    </Button>
                    <Button type="submit" className="bg-amber-600 hover:bg-amber-700">
                      {editingMember ? 'Update Member' : 'Add Member'}
                    </Button>
                  </div>
                </form>
              </DialogContent>
            </Dialog>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-slate-600">Total Team Members</p>
                  <p className="text-3xl font-bold text-slate-800">{teamMembers.length}</p>
                </div>
                <Users className="h-8 w-8 text-blue-600" />
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-slate-600">Admins</p>
                  <p className="text-3xl font-bold text-red-600">
                    {teamMembers.filter(m => m.role === 'admin').length}
                  </p>
                </div>
                <Shield className="h-8 w-8 text-red-600" />
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-slate-600">Managers</p>
                  <p className="text-3xl font-bold text-blue-600">
                    {teamMembers.filter(m => m.role === 'manager').length}
                  </p>
                </div>
                <Settings className="h-8 w-8 text-blue-600" />
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-slate-600">Active Members</p>
                  <p className="text-3xl font-bold text-green-600">
                    {teamMembers.filter(m => m.isActive).length}
                  </p>
                </div>
                <CheckCircle className="h-8 w-8 text-green-600" />
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Filters */}
        <Card className="mb-6">
          <CardContent className="p-6">
            <div className="flex flex-col sm:flex-row gap-4 items-center justify-between">
              <div className="flex items-center space-x-2 w-full sm:w-auto">
                <Search className="h-5 w-5 text-slate-400" />
                <Input
                  type="text"
                  placeholder="Search team members..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full sm:w-80"
                />
              </div>
              
              <div className="flex items-center space-x-2">
                <Filter className="h-5 w-5 text-slate-400" />
                <Select value={roleFilter} onValueChange={setRoleFilter}>
                  <SelectTrigger className="w-40">
                    <SelectValue placeholder="Filter by role" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Roles</SelectItem>
                    <SelectItem value="admin">Admin</SelectItem>
                    <SelectItem value="manager">Manager</SelectItem>
                    <SelectItem value="agent">Agent/Staff</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Team Members Grid */}
        {isLoading ? (
          <Card>
            <CardContent className="p-12 text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-amber-600 mx-auto mb-4"></div>
              <p className="text-slate-600">Loading team members...</p>
            </CardContent>
          </Card>
        ) : filteredMembers.length === 0 ? (
          <Card>
            <CardContent className="p-12 text-center">
              <Users className="h-16 w-16 text-slate-400 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-slate-800 mb-2">No team members found</h3>
              <p className="text-slate-600 mb-6">
                {searchTerm || roleFilter !== 'all'
                  ? 'Try adjusting your search or filters'
                  : 'Add your first team member to get started'
                }
              </p>
              {!searchTerm && roleFilter === 'all' && (
                <Button onClick={() => setIsDialogOpen(true)} className="bg-amber-600 hover:bg-amber-700">
                  <UserPlus className="h-4 w-4 mr-2" />
                  Add First Team Member
                </Button>
              )}
            </CardContent>
          </Card>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
            {filteredMembers.map((member) => (
              <Card key={member.id} className="hover:shadow-xl transition-all duration-300 border-0 shadow-lg">
                <CardContent className="p-6">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center space-x-4">
                      <Avatar className="h-12 w-12">
                        <AvatarImage src={member.avatar} alt={member.fullName} />
                        <AvatarFallback className="bg-amber-100 text-amber-700 font-semibold">
                          {member.fullName.split(' ').map(n => n[0]).join('')}
                        </AvatarFallback>
                      </Avatar>
                      <div>
                        <h4 className="font-semibold text-slate-800">{member.fullName}</h4>
                        <p className="text-sm text-slate-600">@{member.username}</p>
                        <p className="text-sm text-slate-600">{member.department}</p>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Badge className={`${getRoleColor(member.role)} flex items-center space-x-1`}>
                        {getRoleIcon(member.role)}
                        <span className="capitalize">{member.role}</span>
                      </Badge>
                      {member.isActive ? (
                        <CheckCircle className="h-4 w-4 text-green-500" />
                      ) : (
                        <XCircle className="h-4 w-4 text-red-500" />
                      )}
                    </div>
                  </div>

                  <div className="space-y-2 mb-4">
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-slate-600">Email:</span>
                      <span className="font-medium">{member.email}</span>
                    </div>
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-slate-600">Phone:</span>
                      <span className="font-medium">{member.phone}</span>
                    </div>
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-slate-600">Joined:</span>
                      <span className="font-medium">{formatDate(member.joiningDate)}</span>
                    </div>
                    {member.lastLogin && (
                      <div className="flex items-center justify-between text-sm">
                        <span className="text-slate-600">Last Login:</span>
                        <span className="font-medium">{formatDate(member.lastLogin)}</span>
                      </div>
                    )}
                  </div>

                  <div className="grid grid-cols-2 gap-4 mb-4 p-3 bg-slate-50 rounded-lg">
                    <div className="text-center">
                      <div className="text-lg font-bold text-amber-600">{member.packagesCreated}</div>
                      <div className="text-xs text-slate-600">Packages Created</div>
                    </div>
                    <div className="text-center">
                      <div className="text-lg font-bold text-blue-600">{member.clientsManaged}</div>
                      <div className="text-xs text-slate-600">Clients Managed</div>
                    </div>
                  </div>

                  <div className="flex items-center justify-between pt-4 border-t">
                    <div className="flex items-center space-x-2">
                      <Button 
                        variant="outline" 
                        size="sm"
                        onClick={() => handleEdit(member)}
                      >
                        <Edit className="h-4 w-4" />
                      </Button>
                      <Button 
                        variant="outline" 
                        size="sm"
                        className={`${member.isActive ? 'text-red-600 border-red-200 hover:bg-red-50' : 'text-green-600 border-green-200 hover:bg-green-50'}`}
                        onClick={() => toggleMemberStatus(member.id)}
                      >
                        {member.isActive ? 'Deactivate' : 'Activate'}
                      </Button>
                    </div>
                    <Button 
                      variant="outline" 
                      size="sm"
                      className="text-red-600 border-red-200 hover:bg-red-50"
                      onClick={() => handleDelete(member.id)}
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default AdminTeam;